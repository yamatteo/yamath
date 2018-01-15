from flask import Flask
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)
app.secret_key = "oegheofdghvefodvn"

import yamath.views.account
import yamath.views.exercise
import yamath.views.main
import yamath.views.nodes
#import yamath.views.teacher
