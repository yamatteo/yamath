from flask import request
from flask_json import JsonError
from __init__ import app
from decorators import adminRoute
import json

@adminRoute('/api/crud')
def crud(postdata):
    # print("Crud", postdata)
    try:
        method = postdata['method'].lower()
        assert method in ['create', 'read', 'update', 'delete']
    except:
        return dict(status=400, description='Missing or wrong "method" argument.')
    try:
        modelName = postdata['model'].capitalize()
        assert modelName in ['User', 'Node', 'Question']
    except:
        return dict(status=400, description='Missing or wrong "model" argument.')
    try:
        selref = postdata['selref']
    except:
        selref = {}
    try:
        insref = postdata['insref']
    except:
        insref = {}
    try:
        import importlib
        model = getattr(importlib.import_module('models'), modelName)
    except:
        return dict(status=400, description='Can\'t load "%s" model.' % modelName)
    # print(method, model, selref)
    if method == 'create':
        pass
    if method == 'read':
        # print('Reading')
        result = [ json.loads(instance.to_json()) for instance in model.objects.filter(**selref)]
        if len(result) == 0:
            return {"emptyList":True, 'array':[]}
        if len(result) > 0:
            return {'singleResult':(len(result)==1), "array":result}
    if method == 'update':
        pass
    if method == 'delete':
        pass
    return dict(status=500, description='Intentional error', selref=selref, insref=insref, method=method)

@adminRoute("/api/admin")
def admin(postdata):
    import pprint
    # print("adminRoute with postdata:")
    # pprint.pprint(postdata)
    action = postdata.get("action", None)
    selref = postdata.get("selref", {}) or {}
    insref = postdata.get("insref", {}) or {}
    if not (selref.get("_type", None) == "model" or insref.get("_type", None) == "model" ):
        return dict(status=400, description="Argomento _type mancante.")
    try:
        # print("selref", selref)
        # print("insref", insref)
        modelName = (selref.get("_class", None) or insref.get("_class", None)).capitalize()
    except AttributeError as e:
        return dict(status=400, description="Argomento _class mancante. Eccezione:" + str(e))
    import importlib
    model = getattr(importlib.import_module('models'), modelName)
    if action == "filter":
        # print("Running filter action")
        return {"result": [ instance.jref() for instance in model.filterJref(selref) ]}
    elif action == "get":
        try:
            return {"result":model.getJref(selref).jref()}
        except model.DoesNotExist as e:
            return {"status":404, "description":str(e)}
    elif action == "put":
        # if selref:
        #     model.getJson(selref).delete()
        # return {"result":model.newJref(insref).save().jref()}
        ins = model.newJref(insref)
        # ins.save()
        return {"result":ins.jref()}
    elif action == "patch":
        instance = model.getJref(selref)
        instance = model.patchJref(instance, insref)
        return {"result":instance.save().jref()}
    elif action == "delete":
        return {"result":model.getJref(selref).delete()}
    else:
        return dict(status=400, description="No valid action.")
