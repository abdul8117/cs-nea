from flask import Flask, Blueprint, render_template, request, session

import sqlite3

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import get_subject_from_id, get_teacher_name, get_class_info, get_all_subjects

home = Blueprint("home", __name__, url_prefix="/home")

@home.route("/student")
@login_required
@only_students
def student_home():

    if session.get("view") is None:
        session["view"]  = {
            "class_id": None
        }
    else:
        session["view"]["class_id"] = None

    # Get all class details from the database
    # teacher name, number of assignments due, number of overdue assignments

    # Query students_in_classes where username matches with the user logged in.

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    sql = """
    SELECT classes.class_id, classes.title, subjects.subject, classes.teacher, teachers.suffix, teachers.first_name, teachers.surname
    FROM classes
    JOIN students_in_classes
    ON classes.class_id = students_in_classes.class_id
    JOIN teachers
    ON classes.teacher = teachers.username
    JOIN subjects
    ON classes.subject_id = subjects.subject_id
    WHERE students_in_classes.username = ?;
    """
    
    classes = cur.execute(sql, [session["user_info"]["username"]])
    classes = classes.fetchall()
    classes_dict = []
    print(classes)

    for i in range(len(classes)):
        class_ = {
            "id": classes[i][0],
            "title": classes[i][1],
            "subject": classes[i][2],
            "teacher_username": classes[i][3],
            "teacher_suffix": classes[i][4],
            "teacher_first_name": classes[i][5],
            "teacher_surname": classes[i][6]
        }

        classes_dict.append(class_)



    return render_template("home_student.html", user_info=session["user_info"], classes=classes_dict)


@home.route("/teacher")
@login_required
@only_teachers
def teacher_home():
    print(session)

    if session.get("view") is None:
        session["view"]  = {
            "class_id": None
        }
    else:
        session["view"]["class_id"] = None

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    sql = """ 
    SELECT classes.class_id, classes.title, teachers.first_name, teachers.surname, classes.year_group, classes.section, subjects.subject
    FROM classes
    JOIN teachers
    ON classes.teacher = teachers.username
    JOIN subjects
    ON classes.subject_id = subjects.subject_id
    WHERE classes.teacher = ?
    """
    
    classes = cur.execute(sql, [session["user_info"]["username"]]).fetchall()
    classes_dict = []

    for i in range(len(classes)):

        # count the number of students in each class
        num_of_students = cur.execute("SELECT COUNT(*) FROM students_in_classes WHERE class_id = ?", [classes[i][0]]).fetchone()[0]

        class_ = {
            "id": classes[i][0],
            "title": classes[i][1],
            "teacher_first_name": classes[i][2],
            "teacher_surname": classes[i][3],
            "year_group": classes[i][4],
            "section": classes[i][5],
            "subject": classes[i][6],
            "class_size": num_of_students
        }

        classes_dict.append(class_)


    # get all subjects for the create class form
    subjects = get_all_subjects()
    print(subjects)

    return render_template("home_teacher.html", user_info=session["user_info"], classes=classes_dict, subjects=subjects)
