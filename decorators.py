from flask import request
from flask_json import JsonError
from flask_json import as_json
from functools import wraps
from yamath import app, fasthash_dictionary

class adminRoute(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, f):
        @wraps(f)

        @app.route(self.url, methods=["POST"], endpoint=f.__name__)
        @as_json
        def dec_f(*args, **kwargs):
            from yamath.models import User
            postdata = request.get_json(force=True)
            #print(data["username"], data["fasthash"])
            try:
                username = postdata["username"]
                user = User.objects.get(username=username)
                fasthash = postdata["fasthash"]
            except Exception as e:
                print("Raised exception", e)
                raise JsonError(description='Unauthorized request')
            if fasthash_dictionary[username] == fasthash and user.isadmin:
                return f(postdata, *args, **kwargs)
            else:
                # print("not equal")
                raise JsonError(description='Unauthorized request')

        return dec_f

class userRoute(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, f):
        @wraps(f)

        @app.route(self.url, methods=["POST"], endpoint=f.__name__)
        @as_json
        def dec_f(*args, **kwargs):
            from yamath.models import User
            postdata = request.get_json(force=True)
            try:
                username = postdata["username"]
                user = User.objects.get(username=username)
                fasthash = postdata["fasthash"]
            except Exception as e:
                print("exception", e)
                raise JsonError(description='Unauthorized request')
            if fasthash_dictionary[username] == fasthash:
                return f(postdata, *args, **kwargs)
            else:
                raise JsonError(description='Unauthorized request (fasthash mismatch)')

        return dec_f

class freeRoute(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, f):
        @wraps(f)
        @app.route(self.url, methods=["POST"], endpoint=f.__name__)
        @as_json
        def dec_f(*args, **kwargs):
            postdata = request.get_json(force=True)
            return f(postdata, *args, **kwargs)

        return dec_f
