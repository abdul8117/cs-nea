from flask import Flask, Blueprint, render_template, session, redirect, url_for, request

import sqlite3

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import get_subject_from_id, get_class_info, create_class_db

classes = Blueprint("classes", __name__)

@classes.route("/student/class/<int:class_id>")
@login_required
@only_students
def show_student_classpage(class_id):
    class_info = get_class_info(class_id)

    return render_template("class_student.html", user_info=session["user_info"], class_info=class_info)


@classes.route("/teacher/class/<int:class_id>")
@login_required
@only_teachers
def show_teacher_classpage(class_id):
    class_info = get_class_info(class_id)

    return render_template("class_teacher.html", user_info=session["user_info"], class_info=class_info)


@classes.route("/create-class", methods=["GET", "POST"])
@login_required
@only_teachers
def create_class():
    if request.method == "POST":
        class_title = request.form.get("class-title")
        subject_id = request.form.get("subject")
        year_group = request.form.get("year-group")
        section = request.form.get("section")

        if section != "":
            section = None
        
        print(class_title, subject_id, year_group, section)

        create_class_db(class_title, subject_id, year_group, section)

    return redirect(url_for("home.teacher_home"))