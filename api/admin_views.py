from flask import request
from flask_json import JsonError
from __init__ import app
from decorators import adminRoute

@adminRoute('/api/crud')
def crud(postdata):
    print("Crud", postdata)
    try:
        method = postdata['method'].lower()
        assert method in ['create', 'read', 'update', 'delete']
    except:
        return dict(status=400, description='Missing or wrong "method" argument.')
    try:
        selref = postdata['selref']
        assert selref['_type'] == 'model'
    except:
        selref = {}
    try:
        insref = postdata['insref']
        assert insref['_type'] == 'model'
    except:
        insref = {}
    try:
        if (selref):
            modelName = selref['_class'].capitalize()
        elif (insref):
            modelName = insref['_class'].capitalize()
        else:
            raise KeyError
    except:
        return dict(status=400, description='Can\'t deduce "modelName".')
    try:
        import importlib
        model = getattr(importlib.import_module('models'), modelName)
    except:
        return dict(status=400, description='Can\'t load "%s" model.' % modelName)
    print(method, model, selref)
    if method == 'create':
        pass
    if method == 'read':
        print('Reading')
        result = [ instance.jref() for instance in model.filterJref(selref) ]
        if len(result) == 0:
            return {"emptyList":True}
        if len(result) == 1:
            return {"instance":result[0]}
        if len(result) > 1:
            return {'isArray':True, "array":result}
    if method == 'update':
        pass
    if method == 'delete':
        pass
    return dict(status=500, description='Intentional error', selref=selref, insref=insref)

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
