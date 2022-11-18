from flask import Flask, Blueprint, render_template, request, session
from flask_session import Session

import sqlite3

from helpers import login_required

home_bp = Blueprint("name", __name__, url_prefix="/home")


# home = Flask(__name__)
# home.config["SESSION_PERMANENT"] = False
# home.config["SESSION_TYPE"] = "filesystem"
# home.config["SESSION_COOKIE_PATH"] = "/"
# Session(home)


@home_bp.route("/student")
@login_required
def student_home():

    print(session)

    # Get all class details from the database
    # teacher name, number of assignments due, number of overdue assignments

    # Query students_in_classes where username matches with the user logged in.

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    classes = cur.execute("SELECT * FROM students_in_classes WHERE username = ?", [session["user_info"]["username"]])

    print(classes.fetchall())

    return render_template("home_student.html", user_info=session["user_info"])


@home_bp.route("/teacher")
@login_required
def teacher_home():
    print(session)
    return render_template("home_teacher.html", user_info=session["user_info"])
