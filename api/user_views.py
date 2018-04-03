from flask import request
from flask_json import FlaskJSON, JsonError
from mongoengine import *
from __init__ import app, fasthash_dictionary
from decorators import *
from models import *
import json

@userRoute('/api/profile')
def profile(postdata):
    print("profile with", postdata)
    username = postdata.get("username", None)
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        print("Realize there is no profile")
        profile = Profile(user=user)
        profile.save()
    for node in Node.objects.all():
        if node.serial not in profile.means.keys():
            profile.means[node.serial] = 0
    profile.save()
    # nodes = Node.objects()
    return {'profile': json.loads(profile.to_json())}

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

@userRoute('/api/auto_question')
def auto_question(postdata):
    import random
    from pprint import pprint
    username = postdata.get('username', '')
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user).save()
    for node in Node.objects.all():
        if node.serial not in profile.means.keys():
            profile.means[node.serial] = 0
    profile.save()
    means = profile.means
    is_complete = lambda k: means[k] >= 0.9
    is_incomplete = lambda k: means[k] < 0.9
    is_accesible = lambda k: all( is_complete(node.serial) for node in Node.objects.get(serial=k).antes )
    relevant_means = { key:value for (key, value) in profile.means.items() if is_incomplete(key) and is_accesible(key) }
    pprint(relevant_means)
    try:
        node_serial = sorted(relevant_means.keys())[0]
    except:
        node_serial = random.choice([ node.serial for node in Node.objects.all() ])
    node = Node.objects.get(serial=node_serial)
    question = random.choice(list(Question.objects.filter(node=node.id)))
    return {'status':200, 'question':json.loads(question.to_json())}

@userRoute('/api/update_mean')
def update_mean(postdata):
    username = postdata.get('username', '')
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user).save()
    for node in Node.objects.all():
        if node.serial not in profile.means.keys():
            profile.means[node.serial] = 0
    profile.save()
    question_serial = postdata.get('question_serial', '')
    node = Question.objects.get(serial=question_serial).node
    mean_delta = postdata.get('mean_delta', 0)
    profile.means[node.serial] = max(0, min(1, profile.means[node.serial]+mean_delta))
    profile.save()
    return {'status':200}


@freeRoute('/api/node_questions')
def node_questions(postdata):
    node_id = postdata.get('node_id', None)
    node_serial = postdata.get('node_serial', None)
    if node_serial:
        node = Node.objects.get(serial=node_serial)
    elif node_id:
        node = Node.objects.get(id=node_id)
    else:
        return {'status':400, 'description':'Can\'t find the node. No serial or id provided.'}
    questions = Question.objects.filter(node=node.id)
    return {'status':200, 'name':node.name, 'questions':json.loads(questions.to_json())}

@freeRoute('/api/node')
def node(postdata):
    node_serial = postdata.get('node_serial', None)
    if node_serial:
        try:
            node = Node.objects.get(serial=node_serial)
        except Node.DoesNotExist:
            return {'status':400, 'description':'The serial provider is not in the database.'}
    else:
        return {'status':400, 'description':'Can\'t find the node. No serial or id provided.'}
    return {'status':200, 'node':json.loads(node.to_json())}
