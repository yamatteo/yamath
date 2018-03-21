from flask import request
from flask_json import FlaskJSON, JsonError
from mongoengine import *
from __init__ import app, fasthash_dictionary
from decorators import *
from models import *
import json

@userRoute('/api/profile')
def profile(postdata):
    # print("profile with", postdata)
    username = postdata.get("username", None)
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user).save()
    nodes = map(lambda n: n.jref(), Node.objects())
    return {"profile":profile.jref(depth=2), "nodes":nodes}

@freeRoute('/api/question')
def question(postdata):
    question_serial = postdata.get('serial', None)
    question_id = postdata.get('id', None)
    if question_serial:
        question = Question.objects.get(serial=question_serial)
    elif question_id:
        question = Question.objects.get(id=question_id)
    else:
        return {'status':400, 'description':'Can\'t find the question. No serial or id provided.'}
    return {'status':200, 'question':json.loads(question.to_json())}

@freeRoute('/api/node_questions')
def node_questions(postdata):
    node_id = postdata.get('node_id', None)
    node_serial = postdata.get('node_serial', None)
    if node_serial:
        node = Node.objects.get(serial=node_serial)
    elif question_id:
        node = Node.objects.get(id=node_id)
    else:
        return {'status':400, 'description':'Can\'t find the node. No serial or id provided.'}
    questions = Question.objects.filter(node=node.id)
    return {'status':200, 'questions':json.loads(questions.to_json())}
