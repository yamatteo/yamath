production = False
testing = True
database = 'yamath'
from mongoengine import connect

if production:
    connect(host="mongodb://admin:ichigoichie@cluster0-shard-00-00-txgpn.mongodb.net:27017,cluster0-shard-00-01-txgpn.mongodb.net:27017,cluster0-shard-00-02-txgpn.mongodb.net:27017/%s?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin" % database)
else:
    connect(database)
