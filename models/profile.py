from mongoengine import *
from .jsonready import JsonReady

class Mean(EmbeddedDocument, JsonReady):
    node = ReferenceField("Node")
    history = StringField()
    value = FloatField()

class Profile(Document, JsonReady):
    user = ReferenceField("User")
    means = EmbeddedDocumentListField("Mean")

    def __str__(self):
        try:
            return "Profile %s" % self.user.username
        except:
            return "Profile %s" % str(self.id)
