import requests
import unittest
import urllib
import json
from yamath import app

server = 'http://127.0.0.1:5000'

class SessionUser():
    def __init__(self, username="anonymous", fasthash="0000"):
        self.username = username
        self.fasthash = fasthash
    
    def __call__(self, url, data_dict={}, **kwargs):
        data = {"username":self.username, "fasthash":self.fasthash}
        data.update(data_dict)
        data.update(kwargs)
        response = requests.post(server+url, json=data)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            return {"status":500}
            
def curl(url, data={}):
    response = requests.post(server+url, json=data)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        print(response.text)
        return {"status":500}

class TestEmptyDatabase(unittest.TestCase):
    def setUp(self):
        SessionUser()("/danger/erase")
    
    def test_registration(self):
        au = SessionUser()
        
        response = au('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
        response = au('/register', {"username":"other_user", "email":"other_user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
        response = au('/register', {"username":"user", "email":"other__user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
        response = au('/register', {"username":"other__user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
        
    
    def test_object_creation(self):
        au = SessionUser()
        au('/register', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        au("/danger/isadmin", username="admin")
        admin_fasthash = au("/login", username="admin", password="pass")["fasthash"]
        ad = SessionUser("admin", admin_fasthash)
        response = ad("/nodes/new", name="Test node 0", serial="000", antes="[]")
        self.assertEqual(response["status"], 200)
    
    def tearDown(self):
        SessionUser()("/danger/erase")

class TestRegistration(unittest.TestCase):
    """
    Tests user registration.
    """
    
    def test_user_registration(self):
        """
        Tests if a user can be registered if all the data are correct.
        """
        response = curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
        response = curl('/register', {"username":"other_user", "email":"other_user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 200)
    
    
    def test_user_registration_errors(self):
        """
        Tests if users with duplicate username or email can be registered: they should not.
        """
        response = curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        response = curl('/register', {"username":"user", "email":"other_user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
        response = curl('/register', {"username":"other_user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.assertEqual(response["status"], 400)
        
        
    def tearDown(self):
        curl("/danger/erase", {})


class TestLogin(unittest.TestCase):
    """
    Tests login endpoint.
    """
    
    def setUp(self):
        curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        curl('/register', {"username":"other_user", "email":"other_user@example.com", "password1":"pass", "password2":"other_pass"})
    
    
    def test_user_login(self):
        response = curl("/login", {"username":"user", "password":"pass"})
        self.assertEqual(response["status"], 200)
        response = curl("/login", {"username":"user", "password":"other_pass"})
        self.assertEqual(response["status"], 400)
        response = curl("/login", {"username":"other_user", "password":"pass"})
        self.assertEqual(response["status"], 400)
        
        
    def tearDown(self):
        curl("/danger/erase", {})


class TestAccount(unittest.TestCase):
    """
    Tests the possibility to read and change users' account data.
    """
    
    def setUp(self):
        curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        curl('/register', {"username":"other_user", "email":"other_user@example.com", "password1":"other_pass", "password2":"other_pass"})
        self.fasthash = curl("/login", {"username":"user", "password":"pass"})["fasthash"]
    
    
    def test_get_account_info(self):
        response = curl("/account", {"username":"user", "fasthash":self.fasthash})
        self.assertEqual(response["status"], 200)
    
    
    def test_change_username(self):
        """
        You should not be able to change your username.
        """
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"username", "value":"new_user"})
        self.assertEqual(response["status"], 400)
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"username", "value":"other_user"})
        self.assertEqual(response["status"], 400)
    
    
    def test_change_email(self):
        """
        You should be able to change your email, if it is not already taken.
        """
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"email", "value":"newemail@example.com"})
        self.assertEqual(response["status"], 200)
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"email", "value":"other_user@example.com"})
        self.assertEqual(response["status"], 400)
    
    
    def test_change_password(self):
        response = curl("/account/set_password", {"username":"user", "fasthash":self.fasthash, "oldpassword":"notpass", "password1":"newpass", "password2":"newpass"})
        self.assertEqual(response["status"], 400)
        response = curl("/account/set_password", {"username":"user", "fasthash":self.fasthash, "oldpassword":"pass", "password1":"newpass", "password2":"notpass"})
        self.assertEqual(response["status"], 400)
        response = curl("/account/set_password", {"username":"user", "fasthash":self.fasthash, "oldpassword":"pass", "password1":"newpass", "password2":"newpass"})
        self.assertEqual(response["status"], 200)
    
    
    def test_change_marginal_info(self):
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"nickname", "value":"something"})
        self.assertEqual(response["status"], 200)
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"first_name", "value":"something"})
        self.assertEqual(response["status"], 200)
        response = curl("/account/edit", {"username":"user", "fasthash":self.fasthash, "attribute":"last_name", "value":"something"})
        self.assertEqual(response["status"], 200)
    
    
    def tearDown(self):
        curl("/danger/erase", {})

class TestPopulatedDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curl('/register', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        curl("/danger/isadmin", {"username":"admin"})
        admin_fasthash = curl("/login", {"username":"admin", "password":"pass"})["fasthash"]
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node a", "serial":"010", "antes":"[]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node b", "serial":"011", "antes":"[]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node c", "serial":"012", "antes":"['011',]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node d", "serial":"013", "antes":"['011', '012',]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node e", "serial":"014", "antes":"['012', '013', '010',]"})
        
        curl("/question/new", {"username":"admin", "fasthash":admin_fasthash, "name":"Some question", "serial":"0110", "question":"Answer 5.", "answer":"5", "solution":"Solution in 5, just write 5.", "node":"011"})
        curl("/question/new", {"username":"admin", "fasthash":admin_fasthash, "name":"Some question", "serial":"0111", "question":"Answer 4.", "answer":"4", "solution":"Solution in 4, just write 4.", "node":"011"})
        curl("/question/new", {"username":"admin", "fasthash":admin_fasthash, "name":"Some question", "serial":"0120", "question":"Answer 5.", "answer":"5", "solution":"Solution in 5, just write 5.", "node":"012"})
        curl("/question/new", {"username":"admin", "fasthash":admin_fasthash, "name":"Some question", "serial":"0130", "question":"Answer 5.", "answer":"5", "solution":"Solution in 5, just write 5.", "node":"013"})
        curl("/question/new", {"username":"admin", "fasthash":admin_fasthash, "name":"Some question", "serial":"0140", "question":"Answer 5.", "answer":"5", "solution":"Solution in 5, just write 5.", "node":"014"})
        print("Database is ready.")
        
        curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        cls.fasthash = curl("/login", {"username":"user", "password":"pass"})["fasthash"]


    @classmethod
    def tearDownClass(cls):
        curl("/danger/erase", {})
        
        
    def test_nodes(self):
        response = curl("/nodes", {"username":"user", "fasthash":self.fasthash})
        self.assertEqual(response["status"], 200)
    
    def test_question(self):
        response = curl("/question", {"username":"user", "fasthash":self.fasthash, "serial":"011"})
        self.assertEqual(response["status"], 200)
    
    def test_answer_right(self):
        response = curl("/answer", {"username":"user", "fasthash":self.fasthash, "serial":"0111", "answer":"4"})
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["correct"], 1)
    
    def test_answer_wrong(self):
        response = curl("/answer", {"username":"user", "fasthash":self.fasthash, "serial":"0111", "answer":"5"})
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["correct"], 0)
        
        

if __name__ == '__main__':
    unittest.main()