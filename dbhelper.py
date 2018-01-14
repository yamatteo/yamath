import yamath.config as config
from mongoengine import *

class User(Document):
    meta = {'strict':False}
    username = StringField(required=False, unique=True, sparse=True)
    email = StringField(required=True, unique=True)
    salt = StringField(required=True)
    hashed = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    nickname = StringField(max_length=50)
    is_active = BooleanField()
    is_teacher = BooleanField()
    is_admin = BooleanField()
    classrooms = ListField(ReferenceField('Classroom'))
    teacher = ReferenceField('User')
    
    def __str__(self):
        return self.nickname or self.username


class Classroom(Document):
    meta = {"strict":False}
    name = StringField(required=True, unique=True)
    teacher = ReferenceField('User')
    students = ListField(ReferenceField('User'))
    nodes = ListField(ReferenceField('Node'))
    
    def __str__(self):
        return self.name


class Node(Document):
    meta = {"strict":False}
    name = StringField()
    serial = StringField()
    antes = ListField(ReferenceField('Node'))
    posts = ListField(ReferenceField('Node'))
    
    def __str__(self):
        return self.name
    
    @classmethod
    def update_posts(cls, node):
        print("UPDATE POSTS", node, cls.objects(antes__contains=node))
        node.posts = cls.objects.filter(antes=node)
        node.save()


class ExactOpenQuestion(Document):
    meta = {"strict":False}
    name = StringField()
    reference = StringField()
    node = ReferenceField("Node")
    question = StringField()
    answer = StringField()
    solution = StringField()


connect(host="mongodb://admin:ichigoichie@cluster0-shard-00-00-txgpn.mongodb.net:27017,cluster0-shard-00-01-txgpn.mongodb.net:27017,cluster0-shard-00-02-txgpn.mongodb.net:27017/%s?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin" % config.database)
