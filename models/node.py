from mongoengine import *
from .jsonready import JsonReady

class Node(Document, JsonReady):
    name = StringField()
    serial = StringField(unique=True)
    antes = ListField(ReferenceField('Node'))

    def __str__(self):
        return "Node %s" % (self.name or self.serial or str(self.id))
