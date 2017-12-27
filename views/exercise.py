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
from yamath.dbhelper import Classroom
from yamath.dbhelper import DoesNotExist
from yamath.dbhelper import ExactOpenQuestion
from yamath.dbhelper import Node
from yamath.dbhelper import User
from yamath.passwordhelper import PasswordHelper
from yamath import app


@app.route("/exercise/detail/<primary_id>")
@templated("exercise_detail.html")
@teacher_required
def exerciseDetail(primary_id):
    exercise = ExactOpenQuestion.objects.get(id=primary_id)
    return dict(exercise=exercise)

@app.route("/classroom/edit/name/<primary_id>", methods=["POST"])
@teacher_required
def classroomEditName(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    classroom.name = request.form.get('name')
    classroom.save()
    redirect_view = request.form.get('redirect_view') or 'dashboard'
    return redirect(url_for(redirect_view, primary_id=primary_id))

@app.route("/classroom/add/node/<primary_id>", methods=["POST"])
@teacher_required
def classroomAddNode(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    node = Node.objects.get(id=request.form.get("secondary_id"))
    classroom.nodes.append(node)
    classroom.save()
    redirect_view = request.form.get('redirect_view') or 'dashboard'
    return redirect(url_for(redirect_view, primary_id=primary_id))

@app.route("/classroom/add/student/<primary_id>", methods=["POST"])
@teacher_required
def classroomAddStudent(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    student = User.objects.get(id=request.form.get("secondary_id"))
    classroom.students.append(student)
    classroom.save()
    student.classrooms.append(classroom)
    student.save()
    redirect_view = request.form.get('redirect_view') or 'dashboard'
    return redirect(url_for(redirect_view, primary_id=primary_id))

@app.route("/classroom/rem/node/<primary_id>", methods=["POST"])
@teacher_required
def classroomRemNode(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    node = Node.objects.get(id=request.form.get("secondary_id"))
    classroom.nodes.remove(node)
    classroom.save()
    redirect_view = request.form.get('redirect_view') or 'dashboard'
    return redirect(url_for(redirect_view, primary_id=primary_id))

@app.route("/classroom/rem/student/<primary_id>", methods=["POST"])
@teacher_required
def classroomRemStudent(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    student = User.objects.get(id=request.form.get("secondary_id"))
    classroom.students.remove(student)
    classroom.save()
    student.classrooms.remove(classroom)
    student.save()
    redirect_view = request.form.get('redirect_view') or 'dashboard'
    return redirect(url_for(redirect_view, primary_id=primary_id))
    