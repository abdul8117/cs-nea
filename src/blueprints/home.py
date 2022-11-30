from flask import Flask, Blueprint, render_template, request, session

from math import ceil
import sqlite3

from src.helpers import login_required
from src.db_helpers import get_subject_from_id, get_teacher_name

home = Blueprint("home", __name__, url_prefix="/home")

@home.route("/student")
@login_required
def student_home():

    # Get all class details from the database
    # teacher name, number of assignments due, number of overdue assignments

    # Query students_in_classes where username matches with the user logged in.

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    sql_query = """SELECT classes.class_id, classes.title, classes.teacher, classes.subject_id 
                FROM classes
                INNER JOIN students_in_classes ON classes.class_id = students_in_classes.class_id
                WHERE students_in_classes.username = ?"""
    
    # columns: 
    # class_id 0, title 1, teacher-username 2, subject_id 3, subject 4   
    classes = cur.execute(sql_query, [session["user_info"]["username"]])
    classes = classes.fetchall()

    # add subject and teacher names to the lists
    classes = [list(x) for x in classes]
    for i in range(len(classes)):
        classes[i].append(f"{get_subject_from_id(classes[i][3])}")
        teacher_name = get_teacher_name(classes[i][2])
        classes[i][2] = teacher_name[0].capitalize() + " " + teacher_name[1].capitalize()

    print("classes: ", classes)

    return render_template("home_student.html", user_info=session["user_info"], classes=classes, parent_tile_loop_val= int(ceil(len(classes)) / 2))


@home.route("/teacher")
@login_required
def teacher_home():
    print(session)

    # if session["user_info"]["is_student"]:
    #     return redirect("/unauthorised")


    # TODO: USE DICT INSTEAD
    

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    # 0 class id, 1 title, 2 teacher username, 3 subject id, 4 year_group, 5 section 
    classes = cur.execute("SELECT * FROM classes WHERE teacher = ?", [session["user_info"]["username"]]).fetchall()
    classes = [list(x) for x in classes]

    for i in range(len(classes)):
        num_of_students = cur.execute("SELECT COUNT(*) FROM students_in_classes WHERE class_id = ?", [classes[i][0]]).fetchone()[0]
        classes[i].append(num_of_students)
        
    print(classes)

    return render_template("home_teacher.html", user_info=session["user_info"], classes=classes)
