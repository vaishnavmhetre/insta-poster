# Get Instagram Followers

import os

import requests

from DB.Models import Post as DBPost
from DB.Util import Post
from DB.Util import User
from Instagram.Util import Tag


def getNonExistingPost(posts):
    for post in posts:
        if 'image_versions2' in post:
            if not Post.doesPostExistInDB(post):
                return post
    return None


def getImageUrlFromPost(post):
    return post['image_versions2']['candidates'][0]['url']


def parseFileNameFromUrl(url):
    return url.split("/")[-1].split("?")[0]


def downloadAndWriteImage(url, destinationFilePath):
    req = requests.get(url)

    with open(destinationFilePath, 'wb') as file:
        file.write(req.content)


def generateStoragePath(storageDir, fileName):
    return storageDir + "/{}".format(fileName)


def retrieveAndDownloadMedia(storageDir, post):
    url = getImageUrlFromPost(post)
    fileName = parseFileNameFromUrl(url)
    filePath = generateStoragePath(storageDir, fileName)
    downloadAndWriteImage(url, filePath)
    return filePath


def uploadMedia(api, mediaPath, caption):
    api.uploadPhoto(mediaPath, caption=caption)


def registerPostToDB(post, user):
    post = DBPost.create(pk=post['pk'], user=user)
    exhaustUser(user)

    return post


def exhaustUser(user):
    if user.posts.count() >= 10:
        user.exhausted = True
        user.save()


def discardMedia(mediaPath):
    os.remove(mediaPath)


def getPost(api, user):
    posts = api.getTotalUserFeed(user.pk)

    posts = sorted(posts, key=lambda k: k['like_count'], reverse=True)

    post = getNonExistingPost(posts)

    return post


def uploadPost(api, post, user, storageDir, caption):
    mediaPath = retrieveAndDownloadMedia(storageDir, post)
    uploadMedia(api, mediaPath, caption)
    registerPostToDB(post, user)
    discardMedia(mediaPath)


def worker(api, storageDir, captionContent="", tags=[], user=None):
    if user is None:
        user = User.getRandomUser()
        if user is None:
            raise ValueError("No random user received from Repository - returned 'None'")

    post = getPost(api, user)

    caption = """
    {captionContent}
    {linesep}
    ・・・
    {linesep}
    Credits: @{username}
    {linesep}
    ・・・
    {linesep}
    {tagBody}
    """.format(
        captionContent=captionContent,
        username=user.username,
        tagBody=Tag.generateTagsBody(tags),
        linesep='\n'
    )

    uploadPost(api, post, user, storageDir, caption)

    return post
