# This module defines a Password class. It is used to create a password object that contains the user's password, a randomly generated salt, and a hash of the password and salt.

from random import choice
from string import ascii_letters

import hashlib

class Password:
    def __init__(self, password):
        self.password = password
        self.salt = self.generate_salt()
        self.hash = self.create_hash()
    
    @staticmethod
    def generate_salt():
        salt = ""
        length = choice(list(range(10, 21)))
        indexes = [x for x in range(len(ascii_letters))]

        for i in range(length):
            index = choice(indexes)
            salt += ascii_letters[choice(indexes)]
        
        return salt
    
    def create_hash(self):
        # Use the python hashlib library to create and return a hash of the user's password
        pw_hash = hashlib.sha512()
        pw_hash.update(bytes(self.password + self.salt, encoding="utf-16"))
        pw_hash = pw_hash.digest()

        return pw_hash