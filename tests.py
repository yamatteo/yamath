import requests
import unittest
import urllib
import json
from yamath import app

def curl(url, data={}):
    server = 'http://127.0.0.1:5000'
    response = requests.post(server+url, json=data)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        print(response.text)
        return {"status":500}

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

class TestNodes(unittest.TestCase):
    def setUp(self):
        curl('/register', {"username":"admin", "email":"admin@example.com", "password1":"pass", "password2":"pass"})
        curl("/danger/isadmin", {"username":"admin"})
        admin_fasthash = curl("/login", {"username":"admin", "password":"pass"})["fasthash"]
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node a", "serial":"010", "antes":"[]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node b", "serial":"011", "antes":"[]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node c", "serial":"012", "antes":"['011',]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node d", "serial":"013", "antes":"['011', '012',]"})
        curl("/nodes/new", {"username":"admin", "fasthash":admin_fasthash, "name":"node e", "serial":"014", "antes":"['012', '013', '010',]"})
        
        curl('/register', {"username":"user", "email":"user@example.com", "password1":"pass", "password2":"pass"})
        self.fasthash = curl("/login", {"username":"user", "password":"pass"})["fasthash"]
        
        
    def test_whole_tree(self):
        response = curl("/nodes", {"username":"user", "fasthash":self.fasthash})
        self.assertEqual(response["status"], 200)
    
    def tearDown(self):
        curl("/danger/erase", {})
        
        

if __name__ == '__main__':
    unittest.main()