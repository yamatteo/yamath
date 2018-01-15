from yamath.decorators import *
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath.dbhelper import User, Node, ExactOpenQuestion, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app


@app.route("/question", methods=["POST", "GET"])
@login_required
def question():
    import random
    user = User.objects.get(username=request.get_json(force=True)["username"])
    node = Node.objects.get(serial=request.get_json(force=True)["serial"])
    q = random.choice( ExactOpenQuestion.objects.filter(node=node) )
    return json_response(question_data={"name":q.name, "serial":q.serial, "question":q.question, "node":node.serial})


@app.route("/answer", methods=["POST", "GET"])
@login_required
def answer():
    user = User.objects.get(username=request.get_json(force=True)["username"])
    question = ExactOpenQuestion.objects.get(serial=request.get_json(force=True)["serial"])
    answer = request.get_json(force=True)["answer"]
    correct = 1 if (answer == question.answer) else 0
    return json_response(correct=correct, solution=question.solution)
    

@app.route("/question/new", methods=["POST", "GET"])
@admin_required
def question_new():
    data = request.get_json(force=True)
    name = data["name"]
    serial = data["serial"]
    question = data["question"]
    answer = data["answer"]
    solution = data["solution"]
    node = data["node"]
    try:
        node = Node.objects.get(id=node)
    except:
        node = Node.objects.get(serial=node)
    q = ExactOpenQuestion(name=name, serial=serial, question=question, answer=answer, solution=solution, node=node)
    q.save()
    return json_response(description="New question created.")