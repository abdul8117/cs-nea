from flask import Flask, Blueprint, request, redirect, url_for, session, render_template, flash, send_file
from werkzeug.utils import secure_filename

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import DB_PATH, get_class_info, get_list_of_students_in_class

import sqlite3, time, datetime, calendar, os

assignments = Blueprint("assignments", __name__)

@assignments.route("/create-assignment", methods=["POST"])
@login_required
@only_teachers
def create_assignment():
    title = request.form.get("assignment-title")
    if not(title):
        flash("Title not given.")
    
    description = request.form.get("assignment-description")
    due_date = request.form.get("due-date").split("-")

    if not(due_date):
        flash("Due date not given.")
        return redirect(f"teacher/class/{session['view']['class_id']}")

    due_date = datetime.datetime(int(due_date[0]), int(due_date[1]), int(due_date[2]))
    due_date = calendar.timegm(due_date.timetuple())
    date_set = int(time.time())

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql = """
    INSERT INTO assignments 
    (class_id, title, description, date_set, due_date) 
    VALUES(?, ?, ?, ?, ?)
    """

    cur.execute(sql, [session["view"]["class_id"], title, description, date_set, due_date])
    con.commit()

    assignment_id = cur.execute("SELECT assignment_id FROM assignments ORDER BY assignment_id DESC").fetchall()[0][0]

    if request.files:
        file = request.files['attachment']
        filename = secure_filename(file.filename)
        path = f"attachments/{session['view']['class_id']}"
        try:
            os.mkdir(path + f"/{assignment_id}/")
        except FileNotFoundError:
            os.mkdir(path)

        file.save(os.path.join(path + f"/{assignment_id}/", filename))

        sql = """
        INSERT INTO attachments
        (assignment_id, class_id, file_name)
        VALUES(?, ?, ?)
        """
        cur.execute(sql, [assignment_id, session["view"]["class_id"], filename])
        con.commit()

    students = get_list_of_students_in_class()
    for i in students:
        sql = """
        INSERT INTO assigned
        (assignment_id, student_username, submitted, uploaded_work)
        VALUES(?, ?, ?, ?)
        """
        cur.execute(sql, [assignment_id, i[0], False, None])
        con.commit()

    con.close()

    return redirect(f"teacher/class/{session['view']['class_id']}")


@assignments.route("/assignment/<int:class_id>/<int:assignment_id>", methods=["GET"])
@login_required
def assignment_page(class_id, assignment_id):
    class_info = get_class_info(class_id)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    assignments_query = cur.execute("SELECT * FROM assignments WHERE assignment_id = ?", [assignment_id]).fetchone()

    date_set = time.strftime("%d/%m/%y", time.localtime(assignments_query[4]))
    due_date = time.strftime("%d/%m/%y", time.localtime(assignments_query[5]))

    is_overdue = False
    if int(assignments_query[5]) < time.time():
        is_overdue = True
        flash("This assignment is overdue.")

    try:
        # Get attachemnts 
        sql = """
        SELECT attachment_file_path, file_name 
        FROM attachments 
        WHERE assignment_id = ?
        """
        attachment = cur.execute(sql, [assignment_id]).fetchall()[0]
    except:
        # No attachments in this assignment
        attachment = [0, 0]
    
    assignment_info = {
        "id": assignments_query[0],
        "class_id": assignments_query[1],
        "title": assignments_query[2],
        "description": assignments_query[3],
        "attachment_path": attachment[0],
        "attachment_name": attachment[1],
        "date_set": date_set,
        "due_date": due_date,
        "overdue": is_overdue
    }


    # Get list of students who have and haven't marked the assignment as complete.
    sql = """
    SELECT students.first_name, students.surname, assigned.submitted
    FROM students
    JOIN assigned
    ON students.username = assigned.student_username
    WHERE assigned.assignment_id = ?
    """

    students_assigned = cur.execute(sql, [assignment_id]).fetchall()
    con.close()

    submitted = []
    for i in students_assigned:
        if i[2] == 0:
            submitted.append([i[0], i[1], False])
        else:
            submitted.append([i[0], i[1], True])
    
    # check if the student has marked the assignment as complete
    completed = False
    if session["user_info"]["is_student"]:
        for student in submitted:
            if student[0] == session["user_info"]["first_name"].lower() and student[1] == session["user_info"]["surname"].lower():
                if student[2]:
                    completed = True

    return render_template("assignment.html", user_info=session["user_info"], class_info=class_info, assignment=assignment_info, submitted=submitted, completed=completed)

@assignments.route("/assignment/<int:class_id>/<int:assignment_id>/download-attachment")
@login_required
def download_attachment(class_id, assignment_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # get name of file and use that to retrieve the right file from the aattachments folder
    sql = """
    SELECT file_name 
    FROM attachments
    WHERE assignment_id = ?
    """

    file_name = cur.execute(sql, [assignment_id]).fetchone()[0]
    con.close()

    # serve the file from the path in the attachments folder
    return send_file(f"attachments\\{class_id}\\{assignment_id}\\{file_name}")


@assignments.route("/assignment/<int:class_id>/<int:assignment_id>/mark-as-completed")
@login_required
def mark_as_completed(class_id, assignment_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql = """
    UPDATE assigned
    SET submitted = 1
    WHERE assignment_id = ? AND student_username = ?
    """

    cur.execute(sql, [assignment_id, session["user_info"]["username"]])
    con.commit()
    con.close()

    return redirect(f"/assignment/{class_id}/{assignment_id}")