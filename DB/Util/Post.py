from DB.Models import Post


def createPostForUser(user, pk):
    if user is None:
        raise ValueError("Need User object to create post")
    if pk is None or type(pk) is not int:
        raise ValueError("Need pk integer value to create post")
    return Post.create(pk=pk, user=user)


def doesPostExistInDB(onlinePost):
    try:
        Post.get(Post.pk == onlinePost['pk'])
        return True
    except Post.DoesNotExist as e:
        return False
