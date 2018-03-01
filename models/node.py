from mongoengine import *
from .jsonready import JsonReady

class Node(Document, JsonReady):
    name = StringField()
    serial = StringField(unique=True)
    antes = ListField(ReferenceField('Node'))

    def __str__(self):
        return self.serial or str(self.id)

    def __unicode__(self):
        return self.serial or str(self.id)
