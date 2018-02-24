from flask import request
from flask_json import JsonError
from yamath import app
from yamath.decorators import adminRoute

@adminRoute("/api/admin")
def admin(postdata):
    import pprint
    print("adminRoute with postdata:")
    pprint.pprint(postdata)
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
    model = getattr(importlib.import_module('yamath.models'), modelName)
    if action == "filter":
        print("Running filter action")
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
