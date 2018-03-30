import base64
import hashlib
import os
from mongoengine import *
from .jsonready import JsonReady

class User(Document):
    meta = {'strict':False}
    username = StringField(required=True, unique=True)
    email = EmailField(unique=True, sparse=True)
    salt = StringField(required=True)
    hashed = StringField(required=True)
    is_admin = BooleanField(default=False)
    is_teacher = BooleanField(default=False)

    def __str__(self):
        return "User %s" % self.username

    @staticmethod
    def getHash(plain, salt):
        if isinstance(plain, str):
            plain = bytes(plain, "utf-8")
        if isinstance(salt, str):
            salt = bytes(salt, "utf-8")
        return hashlib.pbkdf2_hmac("sha256", plain, salt, 1000).hex()

    @staticmethod
    def getSalt():
        return str(base64.b64encode(os.urandom(12)), 'utf-8')

    @staticmethod
    def validPw(plain, salt, expected):
        if isinstance(plain, str):
            plain = bytes(plain, "utf-8")
        if isinstance(salt, str):
            salt = bytes(salt, "utf-8")
        return hashlib.pbkdf2_hmac("sha256", plain, salt, 1000).hex() == expected
