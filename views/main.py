from yamath.decorators import *
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from yamath.dbhelper import User, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("welcome.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        stored_user = User.objects.get(email=email)
        if PH.validate_password(password, stored_user.salt, stored_user.hashed):
            login_user(stored_user, remember=True)
            return redirect(url_for('dashboard'))
        return redirect(url_for("home"))
    except DoesNotExist:
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password1")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home'))
    try:
        stored_user = User.objects.get(email=email)
        return redirect(url_for('home'))
    except DoesNotExist:
        salt = PH.get_salt()
        hashed = PH.get_hash(pw1, salt)
        User(email=email, salt=salt, hashed=hashed, is_active=True).save()
        return redirect(url_for('home'))
