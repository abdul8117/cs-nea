from flask import Flask, url_for, redirect, render_template, request, session
from flask_session import Session
# from werkzeug import security

from src.blueprints.auth import auth as auth_bp
from src.blueprints.home import home as home_bp
from src.blueprints.profile import profile as profile_bp
from src.blueprints.classes import classes as classes_bp

from src.helpers import login_required

import sqlite3


app = Flask(__name__)

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
app.register_blueprint(classes_bp)


@app.route("/index")
@app.route("/")
@login_required
def index():
    if session["user_info"]["is_student"]:
        return redirect(url_for("home.student_home"))
    else:
        return redirect(url_for("home.teacher_home"))


@app.route("/home/student/assignments")
@login_required
def student_assignments():
    return render_template("all_assignments_student.html", user_info=session["user_info"])


@app.route("/unauthorised")
def unauthorised():
    return "You are not authorised to access this page."