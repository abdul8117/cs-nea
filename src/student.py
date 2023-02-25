from src.user import User, DB_PATH

from flask import session

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
    

    @staticmethod
    def login_query(username):
        # Method to query the user in the database and return the results in a dictionary
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        try:
            db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchone()[0]
            db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]
            salt = cur.execute("SELECT salt FROM students WHERE username = ?", [username]).fetchone()[0]
        except sqlite3.Error:
            return -1 # not found
        
        query = {
            "username": db_username,
            "password_hash": db_password,
            "salt": salt
        }

        return query


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
    