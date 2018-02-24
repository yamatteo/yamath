from flask import request
from flask_json import FlaskJSON, JsonError
from mongoengine import *
from yamath import app, fasthash_dictionary
from yamath.decorators import *
from yamath.models import *

@userRoute('/api/profile')
def profile(postdata):
    print("profile with", postdata)
    username = postdata.get("username", None)
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user).save()
    nodes = map(lambda n: n.jref(), Node.objects())
    return {"profile":profile.jref(depth=2), "nodes":nodes}
