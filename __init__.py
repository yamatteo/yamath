from flask import Flask
from flask import render_template
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)
app.secret_key = "oegheofdghvefodvn"

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("welcome.html")


@app.route("/danger/erase", methods=["POST", "GET"])
def erase():
    from flask_json import json_response
    from yamath.dbhelper import Profile
    from yamath.dbhelper import Node
    from yamath.dbhelper import Question
    Profile.objects.delete()
    Node.objects.delete()
    Question.objects.delete()
    return json_response(description="Everything was deleted.")


@app.route("/danger/isadmin", methods=["POST", "GET"])
def isadmin():
    from flask import request
    from flask_json import json_response
    from yamath.dbhelper import Profile
    username = request.get_json(force=True)["username"]
    u = Profile.objects.get(username=username)
    u.is_admin = True
    u.save()
    return json_response(description="User %s is now admin" % username)


import yamath.profiles.views
import yamath.questions.views
import yamath.nodes.views
