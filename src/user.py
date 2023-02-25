from src.password import Password

from secrets import choice
from string import ascii_letters
import sqlite3

DB_PATH = "db/database.db"

class User:
    def __init__(self, first_name, surname, email, password=""):
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = Password(password)
    
    @staticmethod
    def login_query(username):
        # Method to query the user's password hash and salt in the database and return the results in a dictionary
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        try:
            if "_s" in username:
                db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchone()[0]
                db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]
                salt = cur.execute("SELECT salt FROM students WHERE username = ?", [username]).fetchone()[0]
            elif "_t" in username:
                db_username = cur.execute("SELECT * FROM teachers WHERE username = ?", [username]).fetchone()[0]
                db_password = cur.execute("SELECT password FROM teachers WHERE username = ?", [username]).fetchone()[0]
                salt = cur.execute("SELECT salt FROM teachers WHERE username = ?", [username]).fetchone()[0]
            else:
                return -1
        except:
            print("PASSWORD ERROR")
            return -1 # not found
        
        con.close()

        response = {
            "password_hash": db_password,
            "salt": salt
        }

        return response
    
    @staticmethod
    def check_hash(pw, salt, db_pw_hash):
        # Method to check if the hash of the password submitted matches the one in the database
        import hashlib
        
        pw_hash_check = hashlib.sha512()
        pw_hash_check.update(bytes(pw + salt, encoding="utf-16"))
        
        if db_pw_hash != pw_hash_check.digest():
            # Password does not match
            return -1
        
        # Password matches
        return 1
    
