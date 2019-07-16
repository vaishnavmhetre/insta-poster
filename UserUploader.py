from DB.DBInit import DBInit
from DB.Models import User, Post
from Instagram import Instantiator
from Instagram import User as InstaUser

userList = [
    ..."someusernames"
]

if __name__ == "__main__":

    db = DBInit("./storage/my_db.sqlite").db
    db.create_tables([User, Post])

    api = Instantiator.getApiInstance("your_instagram_username", "your_instagram_password")

    for username in userList:
        print("Assessing User {}".format(username))
        user = InstaUser.getUserFromUsername(api, username)['user']
        try:
            print("Updating User {}".format(username))
            existing_user = User.get(User.pk == user['pk'])
            existing_user.username = user['username']
            existing_user.save()
        except User.DoesNotExist as e:
            print("Creating User {}".format(username))
            created_user = User.create(pk=user['pk'], username=user['username'])
