from yamath.decorators import *
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath.dbhelper import User, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    data = request.get_json(force=True)
    username = data["username"]
    user = User.objects.get(username=username)
    profile = {
        "username":user.username,
        "email":user.email,
        "nickname":user.nickname,
        "first_name":user.first_name,
        "last_name":user.last_name,
    }
    return json_response(profile=profile)

@app.route("/account/edit", methods=["POST", "GET"])
@login_required
def account_edit():
    data = request.get_json(force=True)
    username = data["username"]
    attribute = data["attribute"]
    value = data["value"]
    user = User.objects.get(username=username)
    try:
        assert attribute != "username"
        setattr(user, attribute, value)
        user.save()
        return json_response(description="New value saved")
    except:
        raise JsonError(description="Somehow %s can't be '%s'" % (attribute, value))

@app.route("/account/set_password", methods=["POST", "GET"])
@login_required
def account_set_password():
    data = request.get_json(force=True)
    username = data["username"]
    old_password = data["oldpassword"]
    pw1 = data["password1"]
    pw2 = data["password2"]
    user = User.objects.get(username=username)
    # print("second data", data)
    # print(user.hashed, PH.get_hash(old_password, user.salt))
    try:
        assert user.hashed == PH.get_hash(old_password, user.salt)
        assert pw1 == pw2
        user.hashed = PH.get_hash(pw1, user.salt)
        user.save()
        return json_response(description="New password saved")
    except:
        raise JsonError(description="Somehow password can't be set")
