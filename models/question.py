from mongoengine import *
from .jsonready import JsonReady
# from . import Node


class Question(Document, JsonReady):
    serial = StringField(unique=True)
    node = ReferenceField("Node")
    question = StringField()
    answer = StringField()
    solution = StringField()

    def __str__(self):
        return "Question %s" % (self.serial or str(self.id))
