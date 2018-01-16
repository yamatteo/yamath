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
            "recorded_answers":[
                {
                    "question_serial":ra.question_serial,
                    "datetime":str(ra.datetime),
                    "answer":ra.answer,
                    "correct": 1 if ra.correct else 0,
                }
                for ra in p.recorded_answers
            ],
            "nodes_status":[
                {
                    "node_serial":ns.node_serial,
                    "history":ns.history,
                    "mean":ns.mean,
                }
                for ns in p.nodes_status
            ],
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
            "nodes_status":p.nodes_status,
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
            "nodes_status":p.nodes_status,
        }
    }


@app.route("/status", methods=["GET"])
@login_required
@as_json
def status_get():
    username = dataget("username", request.get_json(force=True))
    profile = Profile.objects.get(username=username)
    pns = {
        s["node_serial"]:{
            'node_serial':s.node_serial,
            'history':s.history,
            'mean':s.mean,
        }
        for s in profile.nodes_status
    }
    return {"nodes_status":pns}

@app.route("/askme/<node_serial>", methods=["GET"])
@login_required
@as_json
def askme(node_serial):
    from random import choice
    from yamath.dbhelper import SingleAnswer
    from datetime import datetime
    username = dataget("username", request.get_json(force=True))
    profile = Profile.objects.get(username=username)
    node = Node.objects.get(serial=node_serial)
    question = choice(Question.objects.filter(node=node))
    profile.recorded_answers.append(
        SingleAnswer(
            question_serial=question.serial,
            datetime=datetime.now(),
            answer=None,
            correct=False,
        )
    )
    profile.save()
    return {
        "question":{
            "question_serial":question.serial,
            "node_serial":node.serial,
            "question_text":question.question,
        }
    }

@app.route("/answer/<question_serial>", methods=["POST"])
@login_required
@as_json
def answer(question_serial):
    username = dataget("username", request.get_json(force=True))
    answer = dataget("answer", request.get_json(force=True))
    profile = Profile.objects.get(username=username)
    question = Question.objects.get(serial=question_serial)
    node = question.node
    try:
        ra = profile.recorded_answers.filter(question_serial=question_serial, answer=None)[0]
        ns = profile.nodes_status.get(node_serial=node.serial)
        ra.answer = answer
        if answer == question.answer:
            ra.correct = True
            ns.history = ('A' + ns.history)[0:20]
            ns.mean = sum( c == 'A' for c in ns.history[0:5] )/5
            ns.save()
            ra.save()
            correct=1
        else:
            ra.correct == False
            ns.history = ('R' + ns.history)[0:20]
            ns.mean = sum( c == 'A' for c in ns.history[0:5] )/5
            ns.save()
            ra.save()
            correct=0
    except (DoesNotExist, IndexError):
        raise JsonError(description="This question was not asked.", status=400)

    return {
        "answer":{
            "question_serial":question.serial,
            "node_serial":node.serial,
            "question_text":question.question,
            "user_answer":answer,
            "question_answer":question.answer,
            "question_solution":question.solution,
            "correct":correct,
        }
    }
