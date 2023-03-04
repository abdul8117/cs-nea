# This module defines a Student class. It inherits from the User class.

from flask import session

from src.user import User, DB_PATH

import sqlite3

class Student(User):
    def __init__(self, first_name, surname, email, password, year_group, section):
        super().__init__(first_name, surname, email, password)
        self.year_group = year_group
        self.section = section
        self.username = self.create_username()
    
    def create_username(self):
        return self.first_name + "." + self.surname[0] + "_s"

    def insert_into_db(self):
        # Method to insert a student into the database 
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        details = (
            self.username, 
            self.first_name, 
            self.surname, 
            self.year_group,
            self.section,
            self.email,
            self.password.hash,
            self.password.salt
        )

        sql = """
        INSERT INTO
        students
        (username, first_name, surname, year_group, section, email, password, salt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            "year_group": self.year_group,
            "section": self.section,
            "email": self.email,
            "is_student": True
        }
    