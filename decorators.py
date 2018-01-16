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
        # print("admin_request", data)
        try:
            username = data["username"]
            fasthash = data["fasthash"]
            # print("break A")
            if PH.fasthash(username, app.secret_key) == fasthash:
                from yamath.dbhelper import Profile
                u = Profile.objects.get(username=username)
                # print("break B")
                if u.is_admin:
                    pass
                else:
                    # print("error 1")
                    raise JsonError(description='Unauthorized request 1')
            else:
                # print("error 2")
                raise JsonError(description='Unauthorized request 2')
        except Exception as e:
            # print("data error3", e)
            raise JsonError(description='Unauthorized request 3')
        return f(*args, **kwargs)

    return dec_f
