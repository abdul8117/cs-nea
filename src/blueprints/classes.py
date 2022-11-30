from flask import Flask, Blueprint, render_template, session

import sqlite3

from src.helpers import login_required
from src.db_helpers import get_subject_from_id, get_class_info

classes = Blueprint("classes", __name__)

@classes.route("/student/class/<int:class_id>")
@login_required
def show_student_classpage(class_id):
    class_info = get_class_info(class_id)

    return render_template("class_student.html", user_info=session["user_info"], class_info=class_info)


@classes.route("/teacher/class/<int:class_id>")
@login_required
def show_teacher_classpage(class_id):
    class_info = get_class_info(class_id)

    return render_template("class_teacher.html", user_info=session["user_info"], class_info=class_info)