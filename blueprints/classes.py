from flask import Flask, Blueprint, render_template, session

import sqlite3

from helpers import login_required
from db_helpers import get_subject_from_id

classes = Blueprint("classes", __name__)

@classes.route("/student/class/<int:class_id>")
@login_required
def show_student_classpage(class_id):

    # get class data
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    class_info = cur.execute("SELECT * FROM classes WHERE class_id = ?", [class_id]).fetchone()
    print("\n\n\nCLASS INFO", class_info)
    class_info = {
        "class_id": class_id,
        "title": class_info[1],
        "teacher": class_info[2],
        "subject": get_subject_from_id(class_info[3]),
        "year_group": class_info[4],
        "section": class_info[5]
    }

    return render_template("class_student.html", user_info=session["user_info"], class_info=class_info)