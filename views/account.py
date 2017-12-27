from yamath.decorators import *
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from yamath.dbhelper import User, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app

@app.route("/account")
@login_required
def account():
    teachers = User.objects.filter(is_teacher=True)
    return render_template("account.html", teachers=teachers)

@app.route("/account/edit/hashed", methods=["POST"])
@login_required
def accountEditHashed():
    pw1 = request.form.get("pw1")
    pw2 = request.form.get("pw2")
    try:
        assert pw1 == pw2
        current_user.hashed = PH.get_hash(pw1, current_user.salt)
        current_user.save()
    except:
        pass
    return redirect(url_for("account"))

@app.route("/account/edit/nickname", methods=["POST"])
@login_required
def accountEditNickname():
    nickname = request.form.get("nickname")
    try:
        current_user.nickname = nickname
        current_user.save()
    except:
        pass
    return redirect(url_for("account"))


@app.route("/account/set/teacher", methods=["POST"])
@login_required
def accountSetTeacher():
    try:
        teacher = User.objects.get(id=request.form.get("secondary_id"))
    except:
        teacher = None
    current_user.teacher = teacher
    current_user.save()
    redirect_view = request.form.get("redirect_view") or "account"
    return redirect(redirect_view)
