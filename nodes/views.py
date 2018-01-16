from yamath.decorators import *
from flask import request
from flask_json import json_response, as_json, JsonError
from yamath.dbhelper import Node, DoesNotExist
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


@app.route("/nodes", methods=["GET"])
@admin_required
@as_json
def nodes_get():
    nt = {
        n.serial:{
            "name":n.name,
            "serial":n.serial,
            "antes":[ an.serial for an in n.antes ],
            # "status":status_or_empty(user, n.serial),
        }
    for n in Node.objects() }
    return {"nodes_data_dict":nt}


@app.route("/nodes", methods=["POST"])
@admin_required
@as_json
def nodes_post():
    data = request.get_json(force=True)
    name = dataget("name", data)
    serial = dataget("serial", data)
    try:
        antes = [ Node.objects.get(serial=s) for s in eval(dataget("antes", data)) ]
    except:
        raise JsonError(status=400, description="List of antes was not wellformed.")
    # print("New node", data)
    n = Node(name=name, serial=serial, antes=antes)
    n.save()
    return {"description":"New node created."}
    
    
@app.route("/nodes/<serial>", methods=["GET"])
@admin_required
@as_json
def node_get(serial):
    n = Node.objects.get(serial=serial)
    return {
        "node_dict":{
            "name":n.name,
            "serial":n.serial,
            "antes":[ n_.serial for n in n.antes ],
        }
    }
    
    
@app.route("/nodes/<serial>", methods=["PATCH"])
@admin_required
@as_json
def node_patch(serial):
    n = Node.objects.get(serial=serial)
    data = request.get_json(force=True)
    n.name = dataget("name", data)
    if (n.serial != dataget("serial", data)):
        raise JsonError(status=400, description="Serials can't change.")
    try:
        n.antes = [ Node.objects.get(serial=s) for s in eval(dataget("antes", data)) ]
    except:
        raise JsonError(status=400, description="List of antes was not wellformed.")
    n.save()
    return {
        "node_dict":{
            "name":n.name,
            "serial":n.serial,
            "antes":[ n_.serial for n_ in n.antes ],
        }
    }
    
    
@app.route("/nodes/<serial>", methods=["DELETE"])
@admin_required
@as_json
def node_delete(serial):
    Node.objects.get(serial=serial).delete()
    return {"description":"Node deleted.",}
