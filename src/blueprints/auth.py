from flask import Flask, Blueprint, url_for, request, redirect, render_template, session, flash
from flask_session import Session

from src.helpers import create_username, generate_salt
from src.db_helpers import insert_user_into_database, get_teacher_info, get_student_info

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
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        
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
        if not(password and confirm_password):
            flash("Password field(s) not given.")
            return redirect(url_for("auth.register"))
        elif password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("auth.register"))
        
        # year group, section
        if not(year_group):
            flash("Year group not given.")
            return redirect(url_for("auth.register"))
        elif not(section):
            flash("Section not given.")
            return redirect(url_for("auth.register"))

        # Create username
        username = create_username(first_name, surname, is_student)
        
        # Hash password using a salt, then encrypt it
        salt = generate_salt()
        pw_hash = hashlib.sha512()
        pw_hash.update(bytes(password + salt, encoding="utf-16"))
        pw_hash = pw_hash.digest() 

        # Insert into DB
        if is_student:
            details = (username, first_name, surname, year_group, section, email, pw_hash, salt)
        else:
            details = (username, first_name, surname, suffix, email, pw_hash, salt)
        
        insert_user_into_database(details, is_student)

        if is_student:
            session["user_info"] = {
                "username": username,
                "first_name": first_name,
                "surname": surname,
                "year_group": year_group,
                "section": section,
                "email": email,
                "is_student": is_student
            }
        else:
            session["user_info"] = {
                "username": username,
                "first_name": first_name,
                "surname": surname,
                "suffix": suffix,
                "email": email,
                "is_student": is_student
            }
            

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
            print("username or password not given")
            return redirect(url_for("auth.login"))
        
        db_username, db_password, salt = None, None, None
        try:
            if "_s" in username:
                db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchone()[0]
                db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]
                salt = cur.execute("SELECT salt FROM students WHERE username = ?", [username]).fetchone()[0]
            elif "_t" in username:
                db_username = cur.execute("SELECT username FROM teachers WHERE username = ?", [username]).fetchone()[0]
                db_password = cur.execute("SELECT password FROM teachers WHERE username = ?", [username]).fetchone()[0]
                salt = cur.execute("SELECT salt FROM teachers WHERE username = ?", [username]).fetchone()[0]
        except:
            pass


        print("\n\n\n")
        print(f"FORM USERNAME - {username}")
        print(f"FORM PASSWORD - {password}")
        print(f"DB USERNAME - {db_username}")
        print(f"DB PASSWORD - {db_password}")
        # print(f"DB SALT {salt}")
        # print(f"DB KEY {key}")
        print("\n\n\n")

        if not(db_username):
            # username not found
            flash("Username not found.")
            return redirect(url_for("auth.login"))
        elif not(db_password):
            flash("Password not given.")

        pw_hash_check = hashlib.sha512()
        pw_hash_check.update(bytes(password + salt, encoding="utf-16"))
        if db_password != pw_hash_check.digest():
            # password is wrong
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