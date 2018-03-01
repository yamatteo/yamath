from pprint import pprint
from __init__ import db_client
import json
import requests
import unittest

def TestingDb():
    from models import User, Node, Question, Profile
    # Users
    User.objects.delete()
    username = 'admin'
    password = 'pass'
    salt = User.getSalt()
    hashed = User.getHash(password, salt)
    User(username=username, salt=salt, hashed=hashed, isadmin=True).save()
    username = 'user'
    password = 'pass'
    salt = User.getSalt()
    hashed = User.getHash(password, salt)
    User(username=username, salt=salt, hashed=hashed, isadmin=False).save()
    # Nodes
    Node.objects.delete()
    n1 = Node(name='Test node 1', serial='T01').save()
    n2 = Node(name='Test node 2', serial='T02').save()
    n3 = Node(name='Test node 3', serial='T03', antes=[n2,]).save()
    n4 = Node(name='Test node 4', serial='T04', antes=[n2,]).save()
    n5 = Node(name='Test node 5', serial='T05', antes=[n3, n4]).save()
    # Questions
    Question.objects.delete()
    for i in range(1, 6):
        for j in range(1, 10):
            Question(
                serial='T0%d%d' % (i, j),
                node=Node.objects.get(serial='T0%d'%i),
                question='Question %d %d' % (i, j),
                answer=str(j),
                solution='Just %d' % j
            ).save()


class SessionUser():
    def __init__(self, username="", password="", server="http://127.0.0.1:5000"):
        self.username = ""
        self.fasthash = ""
        try:
            response = requests.post(server+"/api/login", json={"username":username, "password":password}).json()
        except json.decoder.JSONDecodeError:
            pass
        try:
            self.username = username
            self.fasthash = response["fasthash"]
        except KeyError as e:
            pass
        self.server = server

    def __call__(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.post(self.server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}

class TestSignupAndLogin(unittest.TestCase):
    def setUp(self):
        from models import User
        try:
            User.objects.get(username="testuser").delete()
        except:
            pass

    def test_signup(self):
        au = SessionUser()
        response = au("/api/signup", username="testuser", password="pass", repassword="pass")
        self.assertEqual(response["status"], 200)

    def test_login(self):
        au = SessionUser()
        au("/api/signup", username="testuser", password="pass", repassword="pass")
        response = au("/api/login", username="testuser", password="pass")
        self.assertEqual(response["status"], 200)
        self.assertIn("fasthash", response.keys())

    def tearDown(self):
        from models import User
        try:
            User.objects.get(username="testuser").delete()
        except:
            pass

class TestAdmin(unittest.TestCase):
    ad = None
    u = None
    @classmethod
    def setUpClass(cls):
        super(TestAdmin, cls).setUpClass()
        from models import User
        au = SessionUser()
        au("/api/signup", username="testuser", password="pass", repassword="pass")
        au("/api/signup", username="testadmin", password="pass", repassword="pass")
        ad = User.objects.get(username="testadmin")
        ad.isadmin = True
        ad.save()
        cls.ad = SessionUser("testadmin", "pass")
        cls.u = SessionUser("testuser", "pass")
    def testFilter(self):
        from models import Question
        try:
            Question.objects.get(serial="TestQuestion").delete()
        except Exception as e:
            pass
        res1 = self.ad("/api/admin", action="filter",
            selref={
                "_type":"model",
                "_class":"Question",
                "serial":{"_type":"field", "_class":"StringField", "_value":"TestQuestion"}
            })
        # print("res1", res1)
        try:
            Question(serial="TestQuestion").save()
        except:
            pass
        res2 = self.ad("/api/admin", action="filter",
            selref={
                "_type":"model",
                "_class":"Question",
                "serial":{"_type":"field", "_class":"StringField", "_value":"TestQuestion"}
            })
        self.assertNotEqual(len(res1["result"]), len(res2["result"]))
        Question.objects.get(serial="TestQuestion").delete()
    def testGet(self):
        from models import Question
        try:
            Question(serial="TestQuestion", question="Q?!?").save()
        except:
            pass
        res = self.ad("/api/admin",
            action="get",
            selref={
                "_type":"model",
                "_class":"Question",
                "serial":{"_type":"field", "_class":"StringField", "_value":"TestQuestion"}
            })
        self.assertEqual(res["result"]["question"]["_value"], "Q?!?")
        Question.objects.get(serial="TestQuestion").delete()
    def testPut(self):
        from models import Node
        res = self.ad("/api/admin",
            action="put",
            insref={
                "_type":"model",
                "_class":"Node",
                "name":{"_type":"field", "_class":"StringField", "_value":"TestNode"},
                "serial":{"_type":"field", "_class":"StringField", "_value":"Test0"},
            })
        # print(res)
        self.assertEqual(Node.objects.get(serial="Test0").name, "TestNode")
        Node.objects.get(serial="Test0").delete()
    def testPatch(self):
        from models import Node
        try:
            Node(serial="TEST00").save()
        except:
            pass
        res = self.ad("/api/admin",
            action="patch",
            selref={
                "_type":"model",
                "_class":"Node",
                "serial":{"_type":"field", "_class":"StringField", "_value":"TEST00"}
            },
            insref={
                "_type":"model",
                "_class":"Node",
                "name":{"_type":"field", "_class":"StringField", "_value":"TestNode"},
            },)
        self.assertEqual(res["result"]["name"]["_value"], "TestNode")
        Node.objects.get(serial="TEST00").delete()
    def testDelete(self):
        from models import Node
        try:
            Node(serial="TEST00").save()
        except:
            pass
        res = self.ad("/api/admin",
            action="delete",
            selref={
                "_type":"model",
                "_class":"Node",
                "serial":{"_type":"field", "_class":"StringField", "_value":"TEST00"}
            },)
        with self.assertRaises(Node.DoesNotExist):
            Node.objects.get(serial="TEST00")
        try:
            Node.objects.get(serial="TEST00").delete()
        except:
            pass
    def tearDownClass():
        from models import User
        for username in ("testuser", "tes Node.DoesNotExisttadmin"):
            try:
                User.objects.get(username=username).delete()
            except:
                pass

class TestProfile(unittest.TestCase):
    def testProfile(self):
        ad = SessionUser("admin", "pass")
        response = ad("/api/profile", username=ad.username, fasthash=ad.fasthash)
        nodes = response["nodes"]
        profile = response["profile"]
        # pprint(profile)
        # pprint(nodes)
#
# class TestNodeAndQuestion(unittest.TestCase):
#     def setUpClass():
#         from models import User
#         from models import Node
#         from models import Question
#         for x in ["user", "test0", "test1", "test2", "test3", "test4", "test5"]:
#             try:
#                 User.objects.get(username=x).delete()
#             except:
#                 try:
#                     Node.objects.get(serial=x).delete()
#                 except:
#                     try:
#                         Question.objects.get(serial=x).delete()
#                     except:
#                         pass
#         au = SessionUser()
#         au("/api/signup", username="user", password="pass", repassword="pass")
#         n0 = Node(serial="test0", name="node0").save()
#         n1 = Node(serial="test1", name="node1").save()
#         Question(serial="test2", node=n0.id, question="Q?", answer="5", solution="5!!").save()
#         Question(serial="test3", node=n0.id, question="Q?", answer="5", solution="5!!").save()
#         Question(serial="test4", node=n1.id, question="Q?", answer="5", solution="5!!").save()
#         Question(serial="test5", node=n1.id, question="Q?", answer="5", solution="5!!").save()
#
#     def test_nodelist(self):
#         au = SessionUser()
#         response = au("/api/node/node_list")
#         self.assertIn("node_list", response.keys())
#
#     def test_questionlist(self):
#         au = SessionUser()
#         response = au("/api/node/question_list", node_serial="test0")
#         self.assertEqual(len(response["question_list"]), 2)
#
#     def test_question(self):
#         au = SessionUser()
#         response = au("/api/question/question", question_serial="test3")
#         self.assertEqual(response["question"], "Q?")
#
#     def test_answer(self):
#         au = SessionUser()
#         response = au("/api/question/answer", question_serial="test2", user_answer="5")
#         self.assertEqual(response["correct"], 1)
#         self.assertEqual(response["solution"], "5!!")
#
#
#
#     def tearDownClass():
#         pass
