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

app = Flask(__name__)
app.secret_key = "8524075wreygjdsbcnsso3y6h8egrknbklv0w835u9yhfjdi1"

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(email):
    try:
        return User.objects.get(email=email)
    except:
        return None

import yamath.views.account
import yamath.views.admin
import yamath.views.classroom
import yamath.views.main
import yamath.views.teacher
