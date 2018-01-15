from yamath.decorators import *
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath.dbhelper import User, Node, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app


def status_or_empty(user, serial):
    try:
        return user.nodes_stati[serial]
    except KeyError:
        return {"serial":serial, "history":"", "mean":0}


@app.route("/nodes", methods=["POST", "GET"])
@login_required
def nodes():
    username = request.get_json(force=True)["username"]
    user = User.objects.get(username=username)
    nodes_tree = [ {
        "name":n.name,
        "serial":n.serial,
        "antes":[ an.serial for an in n.antes ],
        "status":status_or_empty(user, n.serial),
    } for n in Node.objects() ]
    return json_response(nodes_tree=nodes_tree)
    

@app.route("/nodes/completed", methods=["POST", "GET"])
@login_required
def nodes_completed():
    username = request.get_json(force=True)["username"]
    user = User.objects.get(username=username)
    nodes_tree = [ {
        "name":n.name,
        "serial":n.serial,
        "antes":[ an.serial for an in n.antes ],
        "status":status_or_empty(user, n.serial),
    } for n in Node.objects() ]
    return json_response(nodes_tree=filter(lambda n: n["status"]["mean"] > 0.9, nodes_tree))
    

@app.route("/nodes/available", methods=["POST", "GET"])
@login_required
def nodes_accessible():
    def completed(serial, nodes_tree):
        return { n["serial"]:n["status"]["mean"] for n in nodes_tree }[serial] > 0.9
    def available(node_data, nodes_tree):
        return all( completed(s, nodes_tree) for s in node_data["antes"] )
    username = request.get_json(force=True)["username"]
    user = User.objects.get(username=username)
    nodes_tree = [ {
        "name":n.name,
        "serial":n.serial,
        "antes":[ an.serial for an in n.antes ],
        "status":status_or_empty(user, n.serial),
    } for n in Node.objects() ]
    return json_response(nodes_tree=filter(lambda n: available(n, nodes_tree), nodes_tree))
    

@app.route("/nodes/new", methods=["POST", "GET"])
@admin_required
def nodes_new():
    data = request.get_json(force=True)
    print("New node", data)
    name, serial, antes = data["name"], data["serial"], eval(data["antes"])
    print("Reading", name, serial, antes)
    antes = [ Node.objects.get(serial=s) for s in antes ]
    n = Node(name=name, serial=serial, antes=antes)
    n.save()
    return json_response(description="New node created.")
