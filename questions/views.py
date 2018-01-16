from yamath.decorators import *
from flask import request
from flask_json import json_response, as_json, JsonError
from yamath.dbhelper import Node, Question, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app


# def status_or_empty(user, serial):
#     try:
#         return user.nodes_stati[serial]
#     except KeyError:
#         return {"serial":serial, "history":"", "mean":0}

def dataget(k, d):
    try:
        return d[k]
    except KeyError:
        raise JsonError(status=400, description="Missing '%s' key in request's data." % k)


@app.route("/questions", methods=["GET"])
@admin_required
@as_json
def questions_get():
    qs = {
        q.serial:{
            "serial":q.serial,
            "node":q.node.serial,
            "question":q.question,
            "answer":q.answer,
            "solution":q.solution,
        }
    for q in Question.objects() }
    return {"questions_data_dict":qs}


@app.route("/questions", methods=["POST"])
@admin_required
@as_json
def questions_post():
    data = request.get_json(force=True)
    serial = dataget("serial", data)
    node = Node.objects.get(serial=dataget("node", data))
    question = dataget("question", data)
    answer = dataget("answer", data)
    solution = dataget("solution", data)
    q = Question(serial=serial, node=node, question=question, answer=answer, solution=solution)
    q.save()
    return {"description":"New question created."}
    
    
@app.route("/questions/<serial>", methods=["GET"])
@admin_required
@as_json
def question_get(serial):
    q = Question.objects.get(serial=serial)
    return {
        "question_dict":{
            "serial":q.serial,
            "node":q.node.serial,
            "question":q.question,
            "answer":q.answer,
            "solution":q.solution,
        }
    }
    
    
@app.route("/questions/<serial>", methods=["PATCH"])
@admin_required
@as_json
def question_patch(serial):
    q = Question.objects.get(serial=serial)
    data = request.get_json(force=True)
    if (q.serial != dataget("serial", data)):
        raise JsonError(status=400, description="Serials can't change.")
    q.node = Node.objects.get(serial=dataget("node", data))
    q.question = dataget("question", data)
    q.answer = dataget("answer", data)
    q.solution = dataget("solution", data)
    q.save()
    return {
        "question_dict":{
            "serial":q.serial,
            "node":q.node.serial,
            "question":q.question,
            "answer":q.answer,
            "solution":q.solution,
        }
    }
    
    
@app.route("/questions/<serial>", methods=["DELETE"])
@admin_required
@as_json
def question_delete(serial):
    Question.objects.get(serial=serial).delete()
    return {"description":"Question deleted.",}
