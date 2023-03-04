from ..user import User
from ..student import Student
from ..teacher import Teacher

from flask import Flask, Blueprint, url_for, request, redirect, render_template, session, flash
from flask_session import Session

from src.helpers import create_username, generate_salt

import sqlite3, hashlib

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    This function is called when a user visits the /register route.
    If the user is simply visiting the site, it is a GET request and the 'else' block of the selection below is executed.
    If the user had submitted a form, then a POST request is sent to the server where the form input will be handled.
    """

    if request.method == "POST":
        # get form data
        first_name = request.form.get("first_name").lower().strip()
        surname = request.form.get("surname").lower().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("confirm_password").strip()
        
        if request.form.get("account_type") == "student":
            is_student = True
            year_group = request.form.get("year-group")
            section = request.form.get("section")
        else:
            is_student = False
            suffix = request.form.get("suffix")
        
        # First and surnames can only be one word and completely alphabetical
        if not(first_name and surname):
            # checks if the name fields are not left blank
            flash("Name(s) not given.")
            return redirect(url_for("auth.register"))
        elif not(first_name.isalpha() and surname.isalpha()):
            flash("Name(s) must be completely alphabteical.")
            return redirect(url_for("auth.register"))
        elif len(first_name.split()) != 1 or len(surname.split()) != 1:
            flash("Name(s) must only be one word.")
            return redirect(url_for("auth.register"))
        
        # email
        if not(email):
            flash("Email not given.")

        # both password fields must be given
        print("HERE", password, confirm_password)
        if not(password and confirm_password):
            flash("Password field(s) not given.")
            return redirect(url_for("auth.register"))
        elif password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("auth.register"))
        

        # Create object
        if is_student:
            # a username and the password hash are created when creating an instance of the student or teacher class
            if not(year_group):
                flash("Year group not given.")
                return redirect(url_for("auth.register"))
            elif not(section):
                flash("Section not given.")
                return redirect(url_for("auth.register"))
            
            student = Student(first_name, surname, email, password, year_group, section)
            student.insert_into_db()
            student.save_into_session()
        else:
            teacher = Teacher(first_name, surname, suffix, email, password)
            teacher.insert_into_db()
            teacher.save_into_session()
        
        return redirect(url_for("index"))
    else:
        # Page accessed via a GET request
        return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    This function is called when a user visits the /login route.
    Just like register(), the webpage is displayed when a GET request is received while a POST requests resuts in form input needing to be handled. 
    """

    if request.method == "POST":
        """
        Check if the username exists.
        Check if the password's hash matches the one in the database.
        """

        # get login details
        username = request.form.get("username")
        password = request.form.get("password")

        # create a cursor to the database
        con = sqlite3.connect("db/database.db", check_same_thread=False)
        cur = con.cursor()

        if not(username and password):
            flash("Username and/or password not given.")
            return redirect(url_for("auth.login"))


        query = User.login_query(username)
        if query == -1:
            flash("User not found.")
            return redirect(url_for("auth.login"))
        
        if User.check_hash(password, query["salt"], query["password_hash"]) == -1:
            flash("Incorrect password.")
            return redirect(url_for("auth.login"))

        if "_s" in username:
            session["user_info"] = {
                "username": username,
                "first_name": cur.execute("SELECT first_name FROM students WHERE username = ?", [username]).fetchone()[0].capitalize(),
                "surname": cur.execute("SELECT surname FROM students WHERE username = ?", [username]).fetchone()[0].capitalize(),
                "email": cur.execute("SELECT email FROM students WHERE username = ?", [username]).fetchone()[0],
                "year_group": cur.execute("SELECT year_group FROM students WHERE username = ?", [username]).fetchone()[0],
                "section": cur.execute("SELECT section FROM students WHERE username = ?", [username]).fetchone()[0],
                "is_student": True,
            }
            
            cur.close()

            return redirect(url_for("home.student_home"))
        else:
            session["user_info"] = {
                "username": username,
                "email": cur.execute("SELECT email FROM teachers WHERE username = ?", [username]).fetchone()[0],
                "first_name": cur.execute("SELECT first_name FROM teachers WHERE username = ?", [username]).fetchone()[0].capitalize(),
                "surname": cur.execute("SELECT surname FROM teachers WHERE username = ?", [username]).fetchone()[0].capitalize(),
                "suffix": cur.execute("SELECT suffix FROM teachers WHERE username = ?", [username]).fetchone()[0],
                "is_student": False,
            }
            
            cur.close()
            
            return redirect(url_for("home.teacher_home"))
    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    
    return redirect("/")