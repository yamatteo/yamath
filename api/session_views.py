from flask import request
from flask_json import FlaskJSON, JsonError
from mongoengine import *
from __init__ import app, fasthash_dictionary
from decorators import *
from models import *

@freeRoute('/api/signup')
def signup(postdata):
    username = postdata.get("username", None)
    password = postdata.get("password", None)
    repassword = postdata.get("repassword", None)
    try:
        if password == repassword:
            ns = User.getSalt()
            nh = User.getHash(password, ns)
            nu = User(username=username, salt=ns, hashed=nh)
            nu.save()
            return {"message":"Utente creato con successo."}
        else:
            raise JsonError(message="Le due password non coincidono.")
    except NotUniqueError:
        raise JsonError(message="Nome utente già in uso.")
    #
    # if User.objects(username=username).count() == 0 :
    #     if password == repassword:
    #         ns = User.getSalt()
    #         nh = User.getHash(password, ns)
    #         nu = User(username=username, salt=ns, hashed=nh)
    #         nu.save()
    #         return {"message":"Utente creato con successo."}
    #     else:
    #         raise JsonError(message="Le due password non coincidono.")
    # else:import requests

@freeRoute("/api/login")
def login(postdata):
    # print("Login request")
    username = postdata.get("username", "")
    password = postdata.get("password", "")
    try:
        u = User.objects.get(username=username)
    except DoesNotExist:
        raise JsonError(message="Nome utente non presente nel database.")
    if User.validPw(password, u.salt, u.hashed):
        fh = User.getSalt()
        fasthash_dictionary[username] = fh
        return {"username": username, "fasthash":fh, "isadmin":u.isadmin}
    else:
        raise JsonError(message="La password non corrisponde.")
