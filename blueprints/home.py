from flask import Flask, Blueprint, render_template, request, session
from flask_session import Session

import sqlite3

from helpers import login_required
from db_helpers import get_subject_from_id, get_teacher_name

home = Blueprint("home", __name__, url_prefix="/home")

@home.route("/student")
@login_required
def student_home():

    # print(session)

    # Get all class details from the database
    # teacher name, number of assignments due, number of overdue assignments

    # Query students_in_classes where username matches with the user logged in.

    con = sqlite3.connect("db/database.db")
    # con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql_query = """SELECT classes.class_id, classes.title, classes.teacher, classes.subject_id 
                FROM classes
                INNER JOIN students_in_classes ON classes.class_id = students_in_classes.class_id
                WHERE students_in_classes.username = ?"""
    
    # columns: 
    # class_id 0, title 1, teacher 2, subject_id 3, subject 4   
    classes = cur.execute(sql_query, [session["user_info"]["username"]])
    classes = classes.fetchall()

    # add subject and teacher names to the lists
    classes_with_subjects = [list(x) for x in classes]
    for i in range(len(classes_with_subjects)):
        classes_with_subjects[i].append(f"{get_subject_from_id(classes_with_subjects[i][3])}")
        teacher_name = get_teacher_name(classes_with_subjects[i][2])
        classes_with_subjects[i][2] = teacher_name[0].capitalize() + " " + teacher_name[1].capitalize()

    return render_template("home_student.html", user_info=session["user_info"], classes=classes_with_subjects, num_of_rows=len(classes))


@home.route("/teacher")
@login_required
def teacher_home():
    print(session)
    return render_template("home_teacher.html", user_info=session["user_info"])
