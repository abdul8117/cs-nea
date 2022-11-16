from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug import security

from blueprints.login import login_blueprint
from blueprints.register import register_blueprint

from helpers import login_required, create_username, insert_user_to_database

import sqlite3


app = Flask(__name__)
con = sqlite3.connect("db/database.db", check_same_thread=False)

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)



@app.route("/")
@login_required
def index():

    print("ALREADY LOGGED IN")

    print(session)

    if session["user_info"]["is_student"]:
        return redirect("/student")
    else:
        return redirect("/teacher")


@app.route("/student")
@login_required
def student_home():

    print(session)

    # Get all class details from the database
    # teacher name, number of assignments due, number of overdue assignments

    # Query students_in_classes where username matches with the user logged in.

    cur = con.cursor()
    classes = cur.execute("SELECT * FROM students_in_classes WHERE username = ?", [session["user_info"]["username"]])

    print(classes.fetchall())

    return render_template("home_student.html", user_info=session["user_info"])


@app.route("/teacher")
@login_required
def teacher_home():
    print(session)
    return render_template("home_teacher.html", user_info=session["user_info"])


# @app.route("/login", methods=["GET", "POST"])
# def login():

#     """
#     This function is called when a user visits the /login route.
#     Just like register(), the webpage is displayed when a GET request is received while a POST requests resuts in form input needing to be handled. 
#     """

#     if request.method == "POST":
#         """
#         Check if the username exists.
#         Check if the password's hash matches the one in the database.
#         """

#         # get login details
#         username = request.form.get("username")
#         password = request.form.get("password")

#         # create a cursor to the database
#         cur = con.cursor()

#         if not(username and password):
#             print("username or password not given")
#             return redirect("/login")

#         # db_user = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchall()[0]
#         # print(db_user)

#         # user_login_info = {
#         #     "username": username,
#         #     "email": db_user[1],
#         #     "first_name": db_user[2],
#         #     "surname": db_user[3],
#         #     "account_type": None
#         # } # TODO validation


#         if "_s" in username:
#             db_username = cur.execute("SELECT * FROM students WHERE username = ?", [username]).fetchone()[0]
#             db_password = cur.execute("SELECT password FROM students WHERE username = ?", [username]).fetchone()[0]        
#         elif "_t" in username:
#             db_username = cur.execute("SELECT username FROM teachers WHERE username = ?", [username]).fetchone()[0]
#             db_password = cur.execute("SELECT password FROM teachers WHERE username = ?", [username]).fetchone()[0]        
#         else:
#             db_username = None
#             db_password = None

        

#         print("\n\n\n")
#         print(f"FORM USERNAME - {username}")
#         print(f"FORM PASSWORD - {password}")
#         print(f"DB USERNAME - {db_username}")
#         print(f"DB PASSWORD - {db_password}")
#         # print(f"DB SALT {salt}")
#         # print(f"DB KEY {key}")
#         print("\n\n\n")

#         # if not(db_username):
#         #     # username not found
#         #     print("// USERNAME DOES NOT MATCH.")
#         #     return render_template("test_page.html", error="USERNAME NOT FOUND")
#         # elif not(security.check_password_hash(db_password, password)):
#         #     # password is wrong
#         #     print("// PASSWORD DOES NOT MATCH.")
#         #     return render_template("test_page.html", error="PASSWORD DOES NOT MATCH")


#         if "_s" in username: 
#             session["user_info"] = {
#                 "username": username,
#                 "first_name": cur.execute("SELECT first_name FROM students WHERE username = ?", [username]).fetchone()[0],
#                 "surname": cur.execute("SELECT surname FROM students WHERE username = ?", [username]).fetchone()[0],
#                 "email": cur.execute("SELECT email FROM students WHERE username = ?", [username]).fetchone()[0],
#                 "year_group": cur.execute("SELECT year_group FROM students WHERE username = ?", [username]).fetchone()[0],
#                 "section": cur.execute("SELECT section FROM students WHERE username = ?", [username]).fetchone()[0],
#                 "is_student": True,
#             }
            
#             return redirect("/student")
#         else:
#             session["user_info"] = {
#                 "username": username,
#                 "email": None, # TODO
#                 "first_name": cur.execute("SELECT first_name FROM teachers WHERE username = ?", [username]).fetchone()[0],
#                 "surname": cur.execute("SELECT surname FROM teachers WHERE username = ?", [username]).fetchone()[0],
#                 "is_student": False,
#                 # "suffix": cur.execute("SELECT suffix FROM teachers WHERE username = ?", [username]).fetchone()[0] # TODO
#             }
            
#             return redirect("/teacher")

#         cur.close()

#     else:
#         return render_template("login.html")




# @app.route("/register", methods=["GET", "POST"])
# def register():

#     """
#     This function is called when a user visits the /register route.
#     If the user is simply visiting the site, it is a GET request and the 'else' block of the selection below is executed.
#     If the user had submitted a form, then a POST request is sent to the server where the form input will be handled.
#     """


#     if request.method == "POST":

#         first_name = request.form.get("first_name").lower().strip()
#         surname = request.form.get("surname").lower().strip()
#         email = request.form.get("email").lower().strip()
#         password = request.form.get("password")
#         confirm_password = request.form.get("confirm-password")
        
#         if request.form.get("account_type") == "student":
#             is_student = True
#             year_group = request.form.get("year-group")
#             section = request.form.get("section")
#         else:
#             is_student = False
#             suffix = request.form.get("suffix")
        
#         # First and surnames can only be one word and completely alphabetical
#         if not(first_name and surname):
#             # checks if the name fields are not left blank
#             print("Name(s) not given")
#             return redirect("/register")
#         elif not(first_name.isalpha() and surname.isalpha()):
#             print("Name(s) must be completely alphabteical")
#             return redirect("/register")
#         elif len(first_name.split()) != 1 or len(surname.split()) != 1:
#             print("Name(s) must be only one word")
#             return redirect("/register")
        
#         # email
#         if not(email):
#             print("Email not given")
#         # TODO Validate email(?)

#         # both password fields must be given
#         if not(password and confirm_password):
#             redirect("/register")
#         elif password != confirm_password:
#             print("Passwords do not match")
#             return redirect("/register")
        
#         # make sure the account type and year group was selected
#         # if not(account_type):
#             # print("Account type must be given")
#             # redirect("/register")
#         # if not(year_group):
#         #     print("Year group must be given")
#         #     redirect("/register")
        
          
#         # Create username
#         username = create_username(first_name, surname, is_student)
        
#         # Hash password using a salt, then encrypt it
#         # salt = generate_salt()
#         # hash_with_salt = hash(password + salt)
#         # key = generate_key(len(str(hash_with_salt)))
#         # encrypted_hash = vernam_cipher.encrypt(hash_with_salt, key)

#         password = security.generate_password_hash(password)

#         # Insert into DB
#         if is_student:
#             details = (username, first_name, surname, email, password, year_group, section)
#         else:
#             details = (username, first_name, surname, suffix, email, password)
#         insert_user_to_database(details, is_student)

#         if is_student: 
#             session["user_info"] = {
#                 "username": username,
#                 "first_name": first_name,
#                 "surname": surname,
#                 "email": email,
#                 "year_group": year_group,
#                 "section": section,
#                 "is_student": is_student
#             }
#         else:
#             session["user_info"] = {
#                 "username": username,
#                 "first_name": first_name,
#                 "surname": surname,
#                 "suffix": suffix,
#                 "email": email,
#                 "is_student": is_student
#             }
            

#         return redirect("/")

#     else:
#         # Page accessed via a GET request
#         return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/profile")
def profile():
    # TODO
    return render_template("profile.html", user_info=session["user_info"])


@app.route("/assignments")
def assignments():
    return render_template("all_assignments_student.html", user_info=session["user_info"])


@app.route("/class")
def class_():
    # TODO
    # class_info variable will be data from the database
    class_info = None 

    return render_template("class_student.html", user_info=session["user_info"], class_info=class_info)


