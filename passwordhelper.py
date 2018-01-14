import base64
import hashlib
import os

class PasswordHelper:
    def fasthash(self, plain, salt):
        return hashlib.sha1((salt+plain).encode('utf-8')).hexdigest()
        
    def get_hash(self, plain, salt):
        if isinstance(plain, str):
            plain = bytes(plain, "utf-8")
        if isinstance(salt, str):
            salt = bytes(salt, "utf-8")
        return hashlib.pbkdf2_hmac("sha256", plain, salt, 1000).hex()

    def get_salt(self):
        return base64.b64encode(os.urandom(20))

    def validate_password(self, plain, salt, expected):
        return self.get_hash(plain, salt) == expected


PH = PasswordHelper()
