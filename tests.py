import requests
import unittest
import json

server = 'http://127.0.0.1:5000'

class SessionUser():
    def __init__(self, username="anonymous", fasthash="0000"):
        self.username = username
        self.fasthash = fasthash
    
    def get(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.get(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}
    
    def patch(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.patch(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}
    
    def post(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.post(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}
    
    def put(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.put(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}
    
    def delete(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.delete(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}

class TestRegistrationAndLogin(unittest.TestCase):
    def setUp(self):
        SessionUser().post("/danger/erase")
    
    def test_registration(self):
        au = SessionUser()
        
        response = au.post('/profiles', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
        response = au.post('/profiles', {"username":"other_user", "email":"other_user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
        response = au.post('/profiles', {"username":"user", "email":"other__user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
        response = au.post('/profiles', {"username":"other__user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
    
    def test_login(self):
        SessionUser().post("/profiles", {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        response = SessionUser().get("/login", username="user", password="pass")
        self.assertIn("fasthash", response)
    
    def tearDown(self):
        SessionUser().post("/danger/erase")

class TestObjectCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        au = SessionUser()
        au.post('/profiles', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        au.post("/danger/isadmin", username="admin")
        admin_fasthash = au.get("/login", username="admin", password="pass")["fasthash"]
        cls.admin = SessionUser("admin", admin_fasthash)
    
    def test_node_creation(self):
        response = self.admin.post("/nodes", name="Test node 0", serial="000", antes="[]")
        self.assertEqual(response["status"], 200)
        response = self.admin.post("/nodes", name="Test node 1", serial="001", antes="['000']")
        self.assertEqual(response["status"], 200)
        response = self.admin.post("/questions", serial='0000', node="000", question="Answer 5", answer="5", solution="Just 5.")
        self.assertEqual(response["status"], 200)
        response = self.admin.post("/questions", serial='0010', node="001", question="Answer 4", answer="4", solution="Just 4.")
        self.assertEqual(response["status"], 200)
    
    @classmethod
    def tearDownClass(cls):
        SessionUser().post("/danger/erase")
        

class TestProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        au = SessionUser()
        au.post('/profiles', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        au.post("/danger/isadmin", username="admin")
        admin_fasthash = au.get("/login", username="admin", password="pass")["fasthash"]
        cls.admin = SessionUser("admin", admin_fasthash)
        au.post("/profiles", {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        user_fasthash = au.get("/login", username="user", password="pass")["fasthash"]
        cls.user = SessionUser("user", user_fasthash)
    
    
    def test_get_profile_info(self):
        response = self.admin.get("/profiles/user")
        self.assertEqual(response["status"], 200)
    
    
    def test_change_password(self):
        response = self.user.patch("/setpassword", {"oldpassword":"notpass", "password1":"newpass", "password2":"newpass"})
        self.assertEqual(response["status"], 400)
        response = self.user.patch("/setpassword", {"oldpassword":"pass", "password1":"newpass", "password2":"notpass"})
        self.assertEqual(response["status"], 400)
        response = self.user.patch("/setpassword", {"oldpassword":"pass", "password1":"newpass", "password2":"newpass"})
        self.assertEqual(response["status"], 200)
        response = self.user.patch("/setpassword", {"oldpassword":"newpass", "password1":"pass", "password2":"pass"})
    
    
    def test_password_reset(self):
        response = self.admin.put("/putpassword/user", password="newpass")
        self.assertEqual(response["status"], 200)
        response = self.user.get("/login", username="user", password="newpass")
        self.assertEqual(response["status"], 200)
    
    @classmethod
    def tearDownClass(cls):
        SessionUser().post("/danger/erase")


class TestPopulatedDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        au = SessionUser()
        au.post('/profiles', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        au.post("/danger/isadmin", username="admin")
        admin_fasthash = au.get("/login", username="admin", password="pass")["fasthash"]
        cls.admin = SessionUser("admin", admin_fasthash)
        au.post("/profiles", {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        user_fasthash = au.get("/login", username="user", password="pass")["fasthash"]
        cls.user = SessionUser("user", user_fasthash)
        
        cls.admin.post("/nodes", {"name":"Node a.", "serial":"010", "antes":"[]"})
        cls.admin.post("/nodes", {"name":"Node b.", "serial":"011", "antes":"[]"})
        cls.admin.post("/nodes", {"name":"Node c.", "serial":"012", "antes":"['011',]"})
        cls.admin.post("/nodes", {"name":"Node d.", "serial":"013", "antes":"['011', '012',]"})
        cls.admin.post("/nodes", {"name":"Node e.", "serial":"014", "antes":"['012', '013', '010',]"})
        
        cls.admin.post("/questions", {"serial":"0110", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"011"})
        cls.admin.post("/questions", {"serial":"0111", "question":"Answer 4.", "answer":"4", "solution":"Solution is 4.", "node":"011"})
        cls.admin.post("/questions", {"serial":"0120", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"012"})
        cls.admin.post("/questions", {"serial":"0130", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"013"})
        cls.admin.post("/questions", {"serial":"0140", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"014"})
        
    def test_nodes(self):
        response = self.admin.get("/nodes")
        self.assertEqual(response["status"], 200)
    
    def test_node(self):
        response = self.admin.get("/nodes/011")
        self.assertEqual(response["status"], 200)
    
    def test_node_patch(self):
        response = self.admin.patch("/nodes/010", name="New name", serial="010", antes="['011']")
        self.assertEqual(response["status"], 200)
        response = self.admin.patch("/nodes/010", name="New name", serial="210", antes="['011']")
        self.assertEqual(response["status"], 400)
    
    def test_questions(self):
        response = self.admin.get("/questions")
        self.assertEqual(response["status"], 200)
    
    def test_question(self):
        response = self.admin.get("/questions/0110")
        self.assertEqual(response["status"], 200)
    
    def test_question_patch(self):
        response = self.admin.patch("/questions/0110", serial="0110", node="013", question="new", answer="new", solution="new")
        self.assertEqual(response["status"], 200)
        response = self.admin.patch("/questions/0110", serial="5110", node="013", question="new", answer="new", solution="new")
        self.assertEqual(response["status"], 400)

    @classmethod
    def tearDownClass(cls):
        cls.admin.post("/danger/erase")
        
class TestUserExperience(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        au = SessionUser()
        au.post('/profiles', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        au.post("/danger/isadmin", username="admin")
        admin_fasthash = au.get("/login", username="admin", password="pass")["fasthash"]
        cls.admin = SessionUser("admin", admin_fasthash)
        au.post("/profiles", {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        user_fasthash = au.get("/login", username="user", password="pass")["fasthash"]
        cls.user = SessionUser("user", user_fasthash)
        
        cls.admin.post("/nodes", {"name":"Node a.", "serial":"010", "antes":"[]"})
        cls.admin.post("/nodes", {"name":"Node b.", "serial":"011", "antes":"[]"})
        cls.admin.post("/nodes", {"name":"Node c.", "serial":"012", "antes":"['011',]"})
        cls.admin.post("/nodes", {"name":"Node d.", "serial":"013", "antes":"['011', '012',]"})
        cls.admin.post("/nodes", {"name":"Node e.", "serial":"014", "antes":"['012', '013', '010',]"})
        
        cls.admin.post("/questions", {"serial":"0110", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"011"})
        cls.admin.post("/questions", {"serial":"0111", "question":"Answer 4.", "answer":"4", "solution":"Solution is 4.", "node":"011"})
        cls.admin.post("/questions", {"serial":"0120", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"012"})
        cls.admin.post("/questions", {"serial":"0130", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"013"})
        cls.admin.post("/questions", {"serial":"0140", "question":"Answer 5.", "answer":"5", "solution":"Solution is 5.", "node":"014"})
    
    def test_status(self):
        response = self.user.get("/status")
        self.assertEqual(response["status"], 200)
    
    def test_askme(self):
        response = self.user.get("/askme/012")
        self.assertEqual(response["status"], 200)
    
    def test_answer(self):
        response = self.user.get("/askme/012")
        response = self.user.post("/answer/0120", answer="5")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["correct"], 1)
        response = self.user.get("/askme/012")
        response = self.user.post("/answer/0120", answer="7")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["correct"], 0)
        response = self.user.post("/answer/0120", answer="5")
        self.assertEqual(response["status"], 400)
        

    @classmethod
    def tearDownClass(cls):
        cls.admin.post("/danger/erase")

if __name__ == '__main__':
    unittest.main()