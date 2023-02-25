from flask import Flask, Blueprint, request, redirect, url_for, session, render_template

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import DB_PATH, get_class_info

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
    cur.close()

    if 'file' in request.files:
        file = request.files.getlist("attachment")
        filename = secure_filename(file.filename)
        path = f"attachments/{session['view']['class_id']}"

        try:
            os.mkdir(path + "/{assignment_id}")
        except FileNotFoundError:
            os.mkdir(path)

        file.save(os.path.join(path, filename))

    return redirect(f"teacher/class/{session['view']['class_id']}")


@assignments.route("/assignment/<int:class_id>/<int:assignment_id>", methods=["GET"])
def assignment_page(class_id, assignment_id):
    class_info = get_class_info(class_id)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    assignments_query = cur.execute("SELECT * FROM assignments WHERE assignment_id = ?", [assignment_id]).fetchone()
    print(assignments_query)

    date_set = time.strftime("%d/%m/%y", time.localtime(assignments_query[4]))
    due_date = time.strftime("%d/%m/%y", time.localtime(assignments_query[5]))

    is_overdue = False
    if int(assignments_query[5]) < time.time():
        is_overdue = True

    try:
        # Get attachemnts 
        sql = """
        SELECT attachment_file_path, file_name 
        FROM attachments 
        WHERE assignment_id = ?
        """
        attachment = cur.execute(sql, [assignment_id]).fetchall()[0]
    except:
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

    return render_template("assignment.html", user_info=session["user_info"], class_info=class_info, assignment=assignment_info)