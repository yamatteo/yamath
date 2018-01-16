from flask import render_template
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath import app
from yamath.dbhelper import Profile, Node, Question, DoesNotExist
from yamath.decorators import *
from yamath.passwordhelper import PH


def dataget(k, d):
    try:
        return d[k]
    except KeyError:
        raise JsonError(status=400, description="Missing '%s' key in request's data." % k)


@app.route("/profiles", methods=["GET"])
@admin_required
@as_json
def profiles_get():
    return {
        "profiles_dict":{
            p.username:{
                "username":p.username,
                "email":p.email,
                "last_login":str(p.last_login),
                "global_mean":p.global_mean,
            }
            for p in Profiles.objects()
        }
    }


@app.route("/profiles", methods=["POST"])
@as_json
def profiles_post():
    data = request.get_json(force=True)
    username = dataget("username", data)
    pw1 = dataget("password1", data)
    pw2 = dataget("password2", data)
    email = dataget("email", data)
    if not pw1 == pw2:
        raise JsonError(status=400, description="Passwords don't match")
    if Profile.objects(email=email).count():
        raise JsonError(status=400, description="Email is already used")
    if Profile.objects(username=username).count():
        raise JsonError(status=400, description="Username is already used")
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1, salt)
    Profile(username=username, email=email, salt=salt, hashed=hashed).save()
    Profile.complete_status(username)
    return dict(description="Profile created", fasthash=PH.fasthash(username, app.secret_key))


@app.route("/profiles/<username>", methods=["GET"])
@admin_required
@as_json
def profile_get(username):
    p = Profile.objects.get(username=username)
    return {
        "profile_dict":{
            "username":p.username,
            "email":p.email,
            "last_login":str(p.last_login),
            "global_mean":p.global_mean,
            "recorded_answers":p.recorded_answers,
            "nodes_stati":p.nodes_stati,
        }
    }


@app.route("/profiles/<username>", methods=["PATCH"])
@admin_required
@as_json
def profile_patch(username):
    p = Profile.objects.get(username=username)
    return {
        "status":400,
        "description":"No profile attribute can be set manually.",
        "profile_dict":{
            "username":p.username,
            "email":p.email,
            "last_login":str(p.last_login),
            "global_mean":p.global_mean,
            "recorded_answers":p.recorded_answers,
            "nodes_stati":p.nodes_stati,
        }
    }


@app.route("/profiles/<username>", methods=["DELETE"])
@admin_required
@as_json
def profile_delete(username):
    Profile.objects.get(username=username).delete()
    return {
        "description":"Profile deleted.",
    }


@app.route("/putpassword/<username>", methods=["PUT"])
@admin_required
@as_json
def putpassword(username):
    p = Profile.objects.get(username=username)
    data = request.get_json(force=True)
    password = dataget("password", data)
    p.hashed = PH.get_hash(password, p.salt)
    p.save()
    return {
        "status":200,
        "description":"Password is changed.",
        "profile_dict":{
            "username":p.username,
            "email":p.email,
            "last_login":str(p.last_login),
            "global_mean":p.global_mean,
            "recorded_answers":p.recorded_answers,
            "nodes_stati":p.nodes_stati,
        }
    }

@app.route("/login", methods=["GET"])
@as_json
def login():
    data = request.get_json(force=True)
    username = dataget("username", data)
    password = dataget("password", data)
    try:
        profile = Profile.objects.get(username=username)
        if PH.validate_password(password, profile.salt, profile.hashed):
            return dict(fasthash=PH.fasthash(username, app.secret_key))
        raise JsonError(description='Incorrect password.')
    except DoesNotExist:
        raise JsonError(description='Unknown username.')


@app.route("/setpassword", methods=["PATCH"])
@login_required
@as_json
def setpassword():
    data = request.get_json(force=True)
    username = dataget("username", data)
    oldpassword = dataget("oldpassword", data)
    password1 = dataget("password1", data)
    password2 = dataget("password2", data)
    p = Profile.objects.get(username=username)
    if not PH.validate_password(oldpassword, p.salt, p.hashed):
        raise JsonError(status=400, description="Old password doesn't match")
    if not password1 == password2:
        raise JsonError(status=400, description="Passwords don't match")
    p.hashed = PH.get_hash(password1, p.salt)
    p.save()
    return {
        "status":200,
        "description":"Password is changed.",
        "profile_dict":{
            "username":p.username,
            "email":p.email,
            "last_login":str(p.last_login),
            "global_mean":p.global_mean,
            "recorded_answers":p.recorded_answers,
            "nodes_stati":p.nodes_stati,
        }
    }


@app.route("/status", methods=["GET"])
@login_required
@as_json
def status_get():
    username = dataget("username", request.get_json(force=True))
    profile = Profile.objects.get(username=username)
    pns = { s["node_serial"]:s for s in profile.nodes_status }
    return {"nodes_status":pns}
    