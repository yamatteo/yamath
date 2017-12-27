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
from yamath.dbhelper import DoesNotExist
from yamath.dbhelper import Classroom
from yamath.dbhelper import Node
from yamath.dbhelper import User
from yamath.passwordhelper import PasswordHelper
from yamath import app

@app.route("/teacher")
@teacher_required
def teacher():
    classrooms = Classroom.objects.filter(teacher=current_user.id)
    return render_template("teacher.html", classrooms=classrooms)

@app.route("/teacher/addClassroom", methods=["POST"])
@teacher_required
def teacherAddClassroom():
    new_name = request.form.get("name")
    try:
        Classroom.objects.get(name=new_name)
    except DoesNotExist:
        user = User.objects.get(email=current_user.email)
        Classroom(name=new_name, teacher=user).save()
    return redirect(url_for("teacher"))

@app.route("/teacher/remClassroom", methods=["POST"])
@teacher_required
def teacherRemClassroom():
    classroom = Classroom.objects.get(name=request.form.get("name"))
    assert classroom.teacher.id == current_user.id
    classroom.delete()
    return redirect(url_for("teacher"))


@app.route("/teacher/classroom/<primary_id>")
@teacher_required
def teacherClassroom(primary_id):
    classroom = Classroom.objects.get(id=primary_id)
    free_students = [ student for student in User.objects(teacher=current_user.id) if classroom not in student.classrooms ]
    free_nodes = [ node for node in Node.objects() if node not in classroom.nodes ]
    return render_template("teacher_classroom.html", classroom=classroom, free_students=free_students, free_nodes=free_nodes)


@app.route("/teacher/classroom/addNode/<classroom_id>", methods=["POST"])
@teacher_required
def teacherClassroomAddNode(classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    node = Node.objects.get(id=request.form.get("node_id"))
    classroom.nodes.append(node)
    classroom.save()
    return redirect(url_for("teacherClassroom", classroom_name=classroom.name))


@app.route("/teacher/classroom/addUser/<classroom_name>", methods=["POST"])
@teacher_required
def teacherClassroomAddUser(classroom_name):
    classroom = Classroom.objects.get(name=classroom_name)
    student = User.objects.get(id=request.form.get("student_id"))
    classroom.students.append(student)
    student.classrooms.append(classroom)
    classroom.save()
    student.save()
    return redirect(url_for("teacherClassroom", classroom_name=classroom.name))


@app.route("/teacher/classroom/remNode/<classroom_id>", methods=["POST"])
@teacher_required
def teacherClassroomRemNode(classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    node = Node.objects.get(id=request.form.get("node_id"))
    classroom.nodes.remove(node)
    classroom.save()
    return redirect(url_for("teacherClassroom", classroom_name=classroom.name))


@app.route("/teacher/classroom/<classroom_name>/remUser", methods=["POST"])
@teacher_required
def teacherClassroomRemUser(classroom_name):
    classroom = Classroom.objects.get(name=classroom_name)
    student = User.objects.get(id=request.form.get("student_id"))
    classroom.students.remove(student)
    student.classrooms.remove(classroom)
    classroom.save()
    student.save()
    return redirect(url_for("teacherClassroom", classroom_name=classroom.name))
