# This module defines the Teacher class. It inherits from the User class.

from src.user import User, DB_PATH

from flask import session

import sqlite3

class Teacher(User):
    def __init__(self, first_name, surname, suffix, email, password):
        super().__init__(first_name, surname, email, password)
        self.suffix = suffix
        self.username = self.create_username()
    
    def create_username(self):
        return self.first_name[0] + "." + self.surname + "_t"
    
    def insert_into_db(self):
        # Method to insert a teacher into the database 
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        details = (
            self.username, 
            self.first_name,
            self.surname, 
            self.suffix,
            self.email,
            self.password.hash,
            self.password.salt
        )
        
        sql = """
        INSERT INTO
        teachers
        (username, first_name, surname, suffix, email, password, salt) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cur.execute(sql, details)
        con.commit()
        con.close()
    
    def save_into_session(self):
        # Save user details into the session dictionary so that it can be easily accessed by other blueprint modules
        session["user_info"] = {
            "username": self.username,
            "first_name": self.first_name,
            "surname": self.surname,
            "suffix": self.suffix,
            "email": self.email,
            "is_student": False,
        }
