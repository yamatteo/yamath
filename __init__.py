from yamath.decorators import *
from flask import Flask

app = Flask(__name__)
app.secret_key = "8524075wreygjdsbcnsso3y6h8egrknbklv0w835u9yhfjdi1"

import yamath.views.account
import yamath.views.admin
import yamath.views.classroom
import yamath.views.main
import yamath.views.teacher
