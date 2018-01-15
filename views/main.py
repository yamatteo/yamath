from flask import render_template
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath import app
from yamath.dbhelper import User, DoesNotExist
from yamath.decorators import *
from yamath.passwordhelper import PH

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("welcome.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    data = request.get_json(force=True)
    #print(data)
    username = data["username"]
    password = data["password"]
    try:
        stored_user = User.objects.get(username=username)
        if PH.validate_password(password, stored_user.salt, stored_user.hashed):
            return json_response(fasthash=PH.fasthash(username, app.secret_key))
        raise JsonError(description='Incorrect password')
    except DoesNotExist:
        raise JsonError(description='Unknown username')

@app.route("/register", methods=["POST", "GET"])
def register():
    data = request.get_json(force=True)
    username = data["username"]
    pw1 = data["password1"]
    pw2 = data["password2"]
    email = data["email"]
    if not pw1 == pw2:
        raise JsonError(description="Passwords don't match")
    if User.objects(email=email).count():
        raise JsonError(description="Email is already used")
    if User.objects(username=username).count():
        raise JsonError(description="Username is already used")
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1, salt)
    User(username=username, email=email, salt=salt, hashed=hashed, is_active=True).save()
    return json_response(description="User created", fasthash=PH.fasthash(username, app.secret_key))


@app.route("/danger/erase", methods=["POST", "GET"])
def erase():
    from yamath.dbhelper import User
    from yamath.dbhelper import Node
    from yamath.dbhelper import ExactOpenQuestion
    User.objects.delete()
    Node.objects.delete()
    ExactOpenQuestion.objects.delete()
    return json_response(description="Everything was deleted.")


@app.route("/danger/isadmin", methods=["POST", "GET"])
def isadmin():
    from yamath.dbhelper import User
    username = request.get_json(force=True)["username"]
    u = User.objects.get(username=username)
    u.is_admin = True
    u.save()
    return json_response(description="User %s is now admin" % username)