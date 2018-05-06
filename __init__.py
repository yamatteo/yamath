# -*- coding: utf-8 -*-
import base64
import hashlib
import os
import sys
# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
# from pprint import pprint
# pprint(dict(os.environ))
# Pare non ci sia più bisogno di tutti questi aggiustamenti, almeno fino al prossimo cambio di contesto
# try:
#     sys.path.append(__path__[0])
#     sys.path.append('rr')
# except NameError:
#     pass

from flask import Flask, render_template, request
from flask_admin import Admin
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS
from mongoengine import connect

app = Flask(__name__, static_folder="./build", template_folder="./build")
app.secret_key = 'super secret key'
# app = Flask(__name__)
# Essendo solo un api, l'applicazione non ha più bisogno di static
json = FlaskJSON(app)
cors = CORS(app)
admin = Admin(app, name='yamath', template_mode='bootstrap3')
from models import *
from flask_admin.contrib.mongoengine import ModelView
admin.add_view(ModelView(User, 'User'))
admin.add_view(ModelView(Node, 'Node'))
admin.add_view(ModelView(Question, 'Question'))
admin.add_view(ModelView(Profile, 'Profile'))


fasthash_dictionary = {}
fasthash_dictionary['mountain_ip'] = '192.168.1.3'
# try:
#     db_client = connect(host=os.environ['MONGODB_URI'])
# except KeyError:
#     db_client = connect('testing')
# app.config["RANDOM_SALT"] = base64.b64encode(os.urandom(20))
# db_client = connect(host="mongodb://admin:ichigoichie@cluster0-shard-00-00-txgpn.mongodb.net:27017,cluster0-shard-00-01-txgpn.mongodb.net:27017,cluster0-shard-00-02-txgpn.mongodb.net:27017/testing?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
# from models import db_client

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_mountain', methods=['POST',])
@as_json
def set_mountain_ip():
    fasthash_dictionary['mountain_ip'] = postdata.get("mountain_ip", '0.0.0.0')
    return {'mountain_ip':fasthash_dictionary['mountain_ip']}

@app.route('/get_mountain')
@as_json
def get_mountain_ip():
    return {'mountain_ip':fasthash_dictionary['mountain_ip']}

from api import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    import unittest
    unittest.main(verbose=False)(verbosity=0).run(suite)
