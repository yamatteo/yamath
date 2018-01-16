import yamath.config as config
from mongoengine import *

class SingleAnswer(EmbeddedDocument):
    question_serial = StringField()
    datetime = DateTimeField()
    answer = StringField()
    correct = BooleanField()

class NodeStatus(EmbeddedDocument):
    node_serial = StringField()
    history = StringField()
    mean = FloatField()

class Profile(Document):
    meta = {'strict':False}
    username = StringField(required=False, unique=True, sparse=True)
    email = EmailField(required=True, unique=True)
    salt = StringField(required=True)
    hashed = StringField(required=True)
    is_admin = BooleanField(default=False)
    last_login = DateTimeField()
    global_mean = FloatField(min_value=0, max_value=1, precision=3, default=0)
    recorded_answers = EmbeddedDocumentListField("SingleAnswer")
    nodes_status = EmbeddedDocumentListField("NodeStatus")

    def __str__(self):
        return self.username

    @classmethod
    def complete_status(cls, username):
        print("entering")
        profile = Profile.objects.get(username=username)
        for node in Node.objects():
            try:
                status = profile.nodes_status.get(node_serial=node.serial)
            except DoesNotExist:
                profile.nodes_status.append(NodeStatus(node_serial=node.serial, history="", mean=0))
                profile.save()


class Node(Document):
    meta = {"strict":False}
    name = StringField()
    serial = StringField(unique=True)
    antes = ListField(ReferenceField('Node'))
    posts = ListField(ReferenceField('Node'))

    def __str__(self):
        return self.name

    @classmethod
    def update_posts(cls, node):
        print("UPDATE POSTS", node, cls.objects(antes__contains=node))
        node.posts = cls.objects.filter(antes=node)
        node.save()


class Question(Document):
    meta = {"strict":False}
    serial = StringField(unique=True)
    node = ReferenceField("Node")
    question = StringField()
    answer = StringField()
    solution = StringField()
