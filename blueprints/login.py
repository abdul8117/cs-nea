from flask import Blueprint, request, redirect, render_template
from flask_session import Session

import sqlite3

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
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
            return redirect("/login")

        if "_s" in username:
            db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchone()[0]
            db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]        
        elif "_t" in username:
            db_username = cur.execute("SELECT username FROM teachers WHERE username = ?", [username]).fetchone()[0]
            db_password = cur.execute("SELECT password FROM teachers WHERE username = ?", [username]).fetchone()[0]        
        else:
            db_username = None
            db_password = None
 

        print("\n\n\n")
        print(f"FORM USERNAME - {username}")
        print(f"FORM PASSWORD - {password}")
        print(f"DB USERNAME - {db_username}")
        print(f"DB PASSWORD - {db_password}")
        # print(f"DB SALT {salt}")
        # print(f"DB KEY {key}")
        print("\n\n\n")

        # if not(db_username):
        #     # username not found
        #     print("// USERNAME DOES NOT MATCH.")
        #     return render_template("test_page.html", error="USERNAME NOT FOUND")
        # elif not(security.check_password_hash(db_password, password)):
        #     # password is wrong
        #     print("// PASSWORD DOES NOT MATCH.")
        #     return render_template("test_page.html", error="PASSWORD DOES NOT MATCH")


        if "_s" in username: 
            session["user_info"] = {
                "username": username,
                "first_name": cur.execute("SELECT first_name FROM students WHERE username = ?", [username]).fetchone()[0],
                "surname": cur.execute("SELECT surname FROM students WHERE username = ?", [username]).fetchone()[0],
                "email": cur.execute("SELECT email FROM students WHERE username = ?", [username]).fetchone()[0],
                "year_group": cur.execute("SELECT year_group FROM students WHERE username = ?", [username]).fetchone()[0],
                "section": cur.execute("SELECT section FROM students WHERE username = ?", [username]).fetchone()[0],
                "is_student": True,
            }
            
            return redirect("/student")
        else:
            session["user_info"] = {
                "username": username,
                "email": None, # TODO
                "first_name": cur.execute("SELECT first_name FROM teachers WHERE username = ?", [username]).fetchone()[0],
                "surname": cur.execute("SELECT surname FROM teachers WHERE username = ?", [username]).fetchone()[0],
                "is_student": False,
                # "suffix": cur.execute("SELECT suffix FROM teachers WHERE username = ?", [username]).fetchone()[0] # TODO
            }
            
            return redirect("/teacher")

        cur.close()

    else:
        return render_template("login.html")
