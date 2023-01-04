from flask import Flask, Blueprint, request, redirect, url_for, session, render_template

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import DB_PATH, get_class_info, get_assignment

import sqlite3, time, datetime, calendar, os

assignments = Blueprint("assignments", __name__)

@assignments.route("/create-assignment", methods=["POST"])
@login_required
@only_teachers
def create_assignment():
    title = request.form.get("assignment-title")
    description = request.form.get("assignment-description")
    date_set = int(time.time())

    due_date = request.form.get("due-date").split("-")
    # due_date = "/".join([due_date[2], due_date[1], due_date[0]])
    due_date = datetime.datetime(int(due_date[0]), int(due_date[1]), int(due_date[2]))
    due_date = calendar.timegm(due_date.timetuple())



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
        files = request.files.getlist("attachments")
        for file in files:
            path = f"C:/Users/abdul/Desktop/GitHub/cs-nea/static/attachments/{session['view']['class_id']}/{assignment_id}"
            sql = """
            BEGIN TRANSACTION
            INSERT INTO attachments
            (assignment_id, class_id, attachment_file_path)
            VALUES (?, ?, ?)
            COMMIT
            """

            cur.execute(sql, [assignment_id, session["view"]["class_id"], path])
            cur.commit()

            try:
                os.mkdir(f"static/attachments/{session['view']['class_id']}")
            except FileExistsError:
                try:
                    os.mkdir(f"static/attachments/{session['view']['class_id']}/{assignment_id}")
                except:
                    pass

            file.save(os.path.join(path, file.filename))

    
    
    
    
    cur.close()

    return redirect(f"teacher/class/{session['view']['class_id']}")


@assignments.route("/assignment/<int:class_id>/<int:assignment_id>", methods=["GET"])
def assignment_page(class_id, assignment_id):
    class_info = get_class_info(class_id)
    assignment_info = get_assignment(assignment_id)


    return render_template("assignment.html", user_info=session["user_info"], class_info=class_info, assignment=assignment_info)