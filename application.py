from flask import Flask, url_for, redirect, render_template, request, session
from flask_session import Session
from werkzeug import security

from blueprints.auth import auth as auth_bp
from blueprints.home import home as home_bp
from blueprints.profile import profile as profile_bp

from helpers import login_required, create_username, insert_user_to_database

import sqlite3


app = Flask(__name__)
# con = sqlite3.connect("db/database.db", check_same_thread=False)

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_PATH"] = "/"
Session(app)


# app.register_blueprint(login_blueprint)
# app.register_blueprint(register_blueprint)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)


@app.route("/index")
@app.route("/")
@login_required
def index():
    if session["user_info"]["is_student"]:
        return redirect(url_for("home.student_home"))
    else:
        return redirect(url_for("home.teacher_home"))


# @app.route("/student")
# @login_required
# def student_home():

#     print(session)

#     # Get all class details from the database
#     # teacher name, number of assignments due, number of overdue assignments

#     # Query students_in_classes where username matches with the user logged in.

#     cur = con.cursor()
#     classes = cur.execute("SELECT * FROM students_in_classes WHERE username = ?", [session["user_info"]["username"]])

#     print(classes.fetchall())

#     return render_template("home_student.html", user_info=session["user_info"])


# @app.route("/teacher")
# @login_required
# def teacher_home():
#     print(session)
#     return render_template("home_teacher.html", user_info=session["user_info"])

# @app.route("/logout")
# def logout():
#     session.clear()

#     return redirect("/")


# @app.route("/profile")
# def profile():
#     # TODO
#     return render_template("profile.html", user_info=session["user_info"])


@app.route("/home/student/assignments")
def student_assignments():
    return render_template("all_assignments_student.html", user_info=session["user_info"])


@app.route("/class")
def class_():
    # TODO
    # class_info variable will be data from the database
    class_info = None 

    return render_template("class_student.html", user_info=session["user_info"], class_info=class_info)


