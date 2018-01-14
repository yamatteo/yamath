from flask import request
from flask_json import JsonError
from functools import wraps
from yamath import app
from yamath.passwordhelper import PH

__all__ = ["login_required", "admin_required"]

def login_required(f):
    @wraps(f)
    
    def dec_f(*args, **kwargs):
        data = request.get_json(force=True)
        #print("data",data)
        #print(data["username"], data["fasthash"])
        try:
            username = data["username"]
            fasthash = data["fasthash"]
            if PH.fasthash(username, app.secret_key) == fasthash:
                pass
            else:
                #print("not equal")
                raise JsonError(description='Unauthorized request')
        except:
            #print("exception", e)
            raise JsonError(description='Unauthorized request')
        return f(*args, **kwargs)

    return dec_f

def admin_required(f):
    @wraps(f)

    @login_required
    def dec_f(*args, **kwargs):
        data = request.get_json(force=True)
        try:
            username = data["username"]
            fasthash = data["fasthash"]
            if PH.fasthash(username, app.secret_key) == fasthash:
                from yamath.dbhelper import User
                u = User.objects.get(username=username)
                if u.is_admin:
                    pass
                else:
                    raise JsonError(description='Unauthorized request')
            else:
                raise JsonError(description='Unauthorized request')
        except:
            raise JsonError(description='Unauthorized request')
        return f(*args, **kwargs)

    return dec_f
