import re


def generateTagsBody(tags):
    body = ""
    tagFormat = "#{tag}"
    for tag in tags:
        body = body + "{tagBody}".format(tagBody=tagFormat.format(tag=tag))
        if tag != tags[-1]:
            body = body + " "

    return body


def parseTagsBodyToList(tagsBody):
    return re.findall(r"#(\w+)", tagsBody)
