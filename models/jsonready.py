from mongoengine import *

class JsonReady:
    def jref(self, depth=1):
        # Json-like reference dictionary
        d = {
            "_type": "model",
            "_class": self._class_name,
            "_name": None,
            "_value": None,
            "_str": self.__str__(),
        }
        if depth==0:
            d.update({"id":self.fieldToJref("id", self._fields["id"], depth)})
        else:
            d.update({ key:self.fieldToJref(key, field, depth) for (key, field) in self._fields.items() })
        return d
    def fieldToJref(self, name, field, depth):
        # print("Jreffing field", name, "of", self, "(is a ObjectIdField? %s)" % isinstance(field, ObjectIdField))
        if isinstance(field, StringField):
            value = getattr(self, name)
        elif isinstance(field, BooleanField):
            value =  True if getattr(self, name) else None
        elif isinstance(field, ReferenceField):
            try:
                value = getattr(self, name).jref(depth-1)
            except AttributeError:
                value = None
        elif isinstance(field, ObjectIdField):
            value = str(getattr(self, name))
        elif isinstance(field, ListField) or isinstance(field, EmbeddedDocumentListField):
            value = []
            for item in getattr(self, name):
                try:
                    value.append(item.jref(depth-1))
                except AttributeError:
                    value.append(item)
        try:
            # print("Value is", value)
            # print("String should be", value["_str"])
            string = value["_str"]
        except:
            string = str(value)
        return {
            "_type": "field",
            "_class":str(type(field).__name__),
            "_name":name,
            "_value":value,
            "_str": "%s: %s" % (name, string),
        }

    @classmethod
    def normJref(cls, jref, superName=None):
        if not isinstance(jref, dict):
            raise ValueError("Object %s is not a jref since it is not a dictionary." % repr(jref))
        _type = jref.get("_type", None)
        if _type not in ("model", "field"):
            raise ValueError("Irregular jref %s" % jref)
        _class = jref.get("_class", None)
        if not _class:
            raise ValueError("Irregular jref %s" % jref)
        _name = jref.get("_name", None) or superName
        _value = jref.get("_value", None)
        if _type == "model" and _class is not None:
            _str = jref.get("_str", jref.get("_class", None))
        elif _type == "field" and _class is not None:
            _str = jref.get("_str", str(_class)+str(_value))
        else:
            raise ValueError("Irregular jref %s" % jref)
        j = {"_type":_type, "_class":_class, "_name":_name, "_value":_value, "_str":_str}
        for (key, value) in jref.items():
            if key[0]!='_':
                j[key] = cls.normJref(value, key)
        return j
    @classmethod
    def jrefToMsa(cls, unnormalizedJref, allowId=True):
        msa = {} # Mongoengine selection arguments
        try:
            jref = cls.normJref(unnormalizedJref)
        except ValueError as e:
            # print("jrefToMsa return \{\} because of unnormalized jref", e)
            return {}
        for (key, item) in jref.items():
            if key[0] == '_' or (key=="id" and allowId==False):
                pass
            else:
                if item["_class"] in ("StringField", "BooleanField", "ObjectIdField"):
                    if item["_value"]:
                        msa[key] = item["_value"]
                elif item["_class"] in ("ReferenceField", ):
                    if item.get("_value", {}).get("id", {}).get("_value", None):
                        msa[key] = item["_value"]["id"]["_value"]
                elif item["_class"] in ("ListField", ):
                    l = []
                    for _item in item.get("_value", []):
                        try:
                            l.append(_item["id"]["_value"])
                        except (KeyError, TypeError) as e:
                            try:
                                from bson import ObjectId
                                l.append(ObjectId(_item))
                            except e:
                                print("Strange case", e)
                                l.append(_item)
                    msa[key] = list(l)
                else:
                    pass
        return msa
    @classmethod
    def filterJref(cls, jref={}):
        msa = cls.jrefToMsa(jref)
        # print("Mongoengine filter with", msa, "...")
        return cls.objects(**msa)
    @classmethod
    def getJref(cls, jref={}):
        msa = cls.jrefToMsa(jref)
        # print("Mongoengine get with", msa, "...")
        return cls.objects.get(**msa)
    @classmethod
    def newJref(cls, jref={}):
        msa = cls.jrefToMsa(jref, allowId=False)
        # print("Mongoengine create with", msa, "...")
        ins = cls(**msa).save()
        return ins
    @classmethod
    def patchJref(cls, instance, jref={}):
        msa = cls.jrefToMsa(jref, allowId=False)
        # print("Mongoengine patch", instance, "with", msa, "...")
        for (key, item) in msa.items():
            setattr(instance, key, item)
        return instance


    def dumpJson(self, depth=1):
        # print("Dumping", self)
        d = {"_model":self._class_name}
        if depth==0:
            d.update({"id":self.fieldToJson(("id", self._fields["id"]), depth=0)})
        else:
            d.update({ key:self.fieldToJson((key, field), depth=depth-1) for (key, field) in self._fields.items() })
        return d
    def fieldToJson(self, item, depth):
        name, field = item
        if isinstance(field, StringField):
            value = getattr(self, name)
        elif isinstance(field, BooleanField):
            value =  True if getattr(self, name) else None
        elif isinstance(field, ReferenceField):
            try:
                value = getattr(self, name).dumpJson(depth)
            except AttributeError:
                value = None
        elif isinstance(field, ObjectIdField):
            value = str(getattr(self, name))
        elif isinstance(field, ListField):
            value = []
            for item in getattr(self, name):
                try:
                    value.append(item.dumpJson(depth))
                except AttributeError:
                    value.append(item)
        return {
            "_field":str(type(field).__name__),
            "_name":name,
            "_value":value,
        }
    @classmethod
    def filterJson(cls, skwargs={}):
        # print("Running filterJson")
        selectionArguments = {}
        for (key, item) in skwargs.items():
            if key in ("_model", ):
                pass
            else:
                if item["_field"] in ("StringField", "BooleanField", "ObjectIdField"):
                    if item.get("_value", None):
                        selectionArguments[key] = item["_value"]
                elif item["_field"] in ("ReferenceField", ):
                    if item.get("_value", {}).get("id", {}).get("_value", None):
                        selectionArguments[key] = item["_value"]["id"]["_value"]
                elif item["_field"] in ("ListField", ):
                    l = []
                    for _item in item.get("_value", []):
                        try:
                            l.append(_item["id"]["_value"])
                        except KeyError as e:
                            l.append(_item)
                    selectionArguments[key] = list(l)
                else:
                    pass
        # print("Returning", cls.objects(**selectionArguments))
        return cls.objects(**selectionArguments)
    @classmethod
    def getJson(cls, skwargs={}):
        # print("Running getJson")
        selectionArguments = {}
        for (key, item) in skwargs.items():
            # print("converting", item)
            if key in ("_model", ):
                pass
            else:
                if item["_field"] in ("StringField", "BooleanField", "ObjectIdField"):
                    if item.get("_value", None):
                        selectionArguments[key] = item["_value"]
                elif item["_field"] in ("ReferenceField", ):
                    if item.get("_value", {}).get("id", {}).get("_value", None):
                        selectionArguments[key] = item["_value"]["id"]["_value"]
                elif item["_field"] in ("ListField", ):
                    l = []
                    for _item in item.get("_value", []):
                        try:
                            l.append(_item["id"]["_value"])
                        except KeyError as e:
                            l.append(_item)
                    selectionArguments[key] = list(l)
                else:
                    pass
        return cls.objects.get(**selectionArguments)
    @classmethod
    def newJson(cls, ikwargs={}):
        # print("Running newJson")
        instanceArguments = {}
        for (key, item) in ikwargs.items():
            # print("converting", item)
            if key in ("_model", "id"):
                pass
            else:
                if item["_field"] in ("StringField", "BooleanField", "ObjectIdField"):
                    if item["_value"]:
                        instanceArguments[key] = item["_value"]
                elif item["_field"] in ("ReferenceField", ):
                    if item["_value"]["id"]["_value"]:
                        instanceArguments[key] = item["_value"]["id"]["_value"]
                elif item["_field"] in ("ListField", ):
                    l = []
                    for _item in item["_value"]:
                        try:
                            l.append(_item["id"]["_value"])
                        except KeyError as e:
                            l.append(_item)
                    instanceArguments[key] = list(l)
                else:
                    pass
        return cls(**instanceArguments)


    @classmethod
    def patchJson(cls, instance, ikwargs={}):
        # print("Running patchJson")
        instanceArguments = {}
        for (key, item) in ikwargs.items():
            # print("converting", item)
            if key in ("_model", "id"):
                pass
            else:
                if item["_field"] in ("StringField", "BooleanField", "ObjectIdField"):
                    if item["_value"]:
                        instanceArguments[key] = item["_value"]
                elif item["_field"] in ("ReferenceField", ):
                    if item["_value"]["id"]["_value"]:
                        instanceArguments[key] = item["_value"]["id"]["_value"]
                elif item["_field"] in ("ListField", ):
                    l = []
                    for _item in item["_value"]:
                        try:
                            l.append(_item["id"]["_value"])
                        except KeyError as e:
                            l.append(_item)
                    instanceArguments[key] = list(l)
                else:
                    pass
        for (key, item) in instanceArguments.items():
            setattr(instance, key, item)
        return instance
