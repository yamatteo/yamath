from yamath.decorators import *
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from yamath.dbhelper import User, Node, DoesNotExist
from yamath.passwordhelper import PH
from yamath import app


@app.route("/nodes", methods=["POST", "GET"])
@login_required
def nodes():
    username = request.get_json(force=True)["username"]
    nodes_tree = [ {"name":n.name, "serial":n.serial, "antes":[ an.serial for an in n.antes ]} for n in Node.objects() ]
    return json_response(nodes_tree=nodes_tree)

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
