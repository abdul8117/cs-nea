from flask import Flask, Blueprint, request, redirect, url_for, session

from src.helpers import login_required, only_students, only_teachers
from src.db_helpers import DB_PATH

import sqlite3, time

assignments = Blueprint("assignments", __name__)

@assignments.route("/create-assignment", methods=["POST"])
@login_required
@only_teachers
def create_assignment():
    title = request.form.get("assignment-title")
    description = request.form.get("assignment-description")
    date_set = int(time.time())

    due_date = request.form.get("due-date").split("-")
    due_date = "/".join([due_date[2], due_date[1], due_date[0]])

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql_query = """
    INSERT INTO assignments 
    (class_id, title, description, date_set, due_date) 
    VALUES(?, ?, ?, ?, ?)
    """

    cur.execute(sql_query, [session["view"]["class_id"], title, description, date_set, due_date])
    con.commit()
    cur.close()

    return redirect(f"teacher/class/{session['view']['class_id']}")