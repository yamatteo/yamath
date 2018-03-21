from .node import Node
from .profile import Profile
from .question import Question
from .user import User

#db_client = connect(host="mongodb://admin:ichigoichie@cluster0-shard-00-00-txgpn.mongodb.net:27017,cluster0-shard-00-01-txgpn.mongodb.net:27017,cluster0-shard-00-02-txgpn.mongodb.net:27017/testing?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
# db_client = connect("testing")
from mongoengine import connect
from dotenv import load_dotenv
load_dotenv('/home/yamatteo/yamath/.env')
import os
try:
    print(os.environ)
    db_client = connect(host=os.environ['MONGODB_URI'])
except KeyError:
    db_client = connect('testing')
