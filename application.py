from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug import security

import sqlite3

from helpers import login_required, generate_salt, create_username, insert_user_to_database
import vernam_cipher

app = Flask(__name__)

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    # TODO
    # if session["user_info"] == "student":
    #     redirect("/student-home")
    # elif session["user-info"] == "teacher":
    #     redirect("/teacher-home")
    # else:
    #     # what if the form was meddled with?
    #     pass

    print("ALREADY LOGGED IN")

    if session["account_type"] == "student":
        return redirect("/student")
    else:
        return redirect("/teacher")

        
@app.route("/student")
@login_required
def student_home():
    return render_template("student_home.html", user_info=session["user_info"])


@app.route("/teacher")
# @login_required
def teacher_home():
    print(session)
    return render_template("teacher_home.html", user_info=session["user_info"])


@app.route("/login", methods=["GET", "POST"])
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

        # connect to database
        con = sqlite3.connect("db/database.db")
        cur = con.cursor()

        if not(username and password):
            print("username or password not given")
            return redirect("/login")

        db_user = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchall()[0]
        print(db_user)

        user_login_info = {
            "username": username,
            "email": db_user[1],
            "first_name": db_user[2],
            "surname": db_user[3],
            "account_type": None
        } # TODO validation

        if "_s" in username:
            try:
                db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchall()
                user_login_info["account_type"] = "student"
            except:
                return render_template("test_page.html", error="USERNAME DOES NOT MATCH")

            try:
                db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]
                # key = cur.execute("SELECT key FROM students WHERE username = ?", [username]).fetchone()[0]
                # salt = cur.execute("SELECT salt FROM students WHERE username = ?", [username]).fetchone()[0]
            except:
                return render_template("test_page.html", error="PASSWORD DOES NOT MATCH")
        
        elif "_t" in username:
            db_username = cur.execute("SELECT username FROM teachers WHERE username = ?", [username]).fetchone()[0]
            user_login_info["account_type"] = "teacher"
            db_password = cur.execute("SELECT password FROM teachers WHERE username = ?", [username]).fetchone()[0]
            # key = cur.execute("SELECT key FROM teachers WHERE username = ?", [username]).fetchone()[0]
            # salt = cur.execute("SELECT salt FROM teachers where username = ?", [username]).fetchone()[0]
        
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

        # hash_form_pw = vernam_cipher.encrypt(str(hash(password + salt)), key)
        # print(hash_form_pw)

        if not(db_username):
            # username not found
            print("// USERNAME DOES NOT MATCH.")
            return render_template("test_page.html", error="USERNAME NOT FOUND")
        elif not(security.check_password_hash(db_password, password)):
            # password is wrong
            print("// PASSWORD DOES NOT MATCH.")
            return render_template("test_page.html", error="PASSWORD DOES NOT MATCH")

        session["user_info"] = user_login_info

        return redirect("/student")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    """
    This function is called when a user visits the /register route.
    If the user is simply visiting the site, it is a GET request and the 'else' block of the selection below is executed.
    If the user had submitted a form, then a POST request is sent to the server where the form input will be handled.
    """


    if request.method == "POST":

        first_name = request.form.get("first_name").lower().strip()
        surname = request.form.get("surname").lower().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        # year_group = request.form.get("year-group")
        account_type = request.form.get("account_type")

        print(f"ACCOUNT TYPE: {account_type}")

        
        # First and surnames can only be one word and completely alphabetical
        if not(first_name and surname):
            # checks if the name fields are not left blank
            print("Name(s) not given")
            return redirect("/register")
        elif not(first_name.isalpha() and surname.isalpha()):
            print("Name(s) must be completely alphabteical")
            return redirect("/register")
        elif len(first_name.split()) != 1 or len(surname.split()) != 1:
            print("Name(s) must be only one word")
            return redirect("/register")
        
        # email
        if not(email):
            print("Email not given")
        # TODO Validate email(?)

        # both password fields must be given
        if not(password and confirm_password):
            redirect("/register")
        elif password != confirm_password:
            print("Passwords do not match")
            return redirect("/register")
        
        # make sure the account type and year group was selected
        if not(account_type):
            print("Account type must be given")
            redirect("/register")
        # if not(year_group):
        #     print("Year group must be given")
        #     redirect("/register")
        
          
        # Create username
        username = create_username(first_name, surname, account_type)
        
        # Hash password using a salt, then encrypt it
        # salt = generate_salt()
        # hash_with_salt = hash(password + salt)
        # key = generate_key(len(str(hash_with_salt)))
        # encrypted_hash = vernam_cipher.encrypt(hash_with_salt, key)

        password = security.generate_password_hash(password)

        # Insert into DB
        if account_type == "student":
            details = (username, email, first_name, surname, password, None)
        elif account_type == "teacher":
            details = (username, email, first_name, surname, password)
        insert_user_to_database(details, account_type)

        session["user_info"] = {
            "username": username,
            "first_name": first_name,
            "surname": surname,
            "account_type": account_type,
            "year_group": None
        }

        return redirect("/")

        # if session["user_info"]["username"][-1] == "t":
        #     return render_template("teacher_home.html", details=session["user_info"])
        # else:
        #     return render_template("student_home.html", details=session["user_info"])

    else:
        # Page accessed via a GET request
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/") 