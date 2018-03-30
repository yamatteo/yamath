from mongoengine import *

class Profile(Document):
    user = ReferenceField("User")
    means = DictField()


    def __str__(self):
        try:
            return "Profile %s" % self.user.username
        except:
            return "Profile %s" % str(self.id)
