from flask import session

import sqlite3


DB_PATH = "db/database.db"


def insert_user_into_database(details, is_student):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if is_student:
        cur.execute("INSERT INTO students (username, first_name, surname, year_group, section, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", details)
    else:
        cur.execute("INSERT INTO teachers (username, first_name, surname, suffix, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?)", details)
    con.commit()
    con.close()


def get_subject_from_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    subject = cur.execute("SELECT subject FROM subjects WHERE subject_id = ?", [id]).fetchone()[0]

    return subject


def get_teacher_name(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    teacher_name = cur.execute("SELECT first_name, surname FROM teachers WHERE username = ?", [username]).fetchall()[0]
    print(teacher_name)

    return teacher_name[0].capitalize() + " " + teacher_name[1].capitalize()


def get_student_info(username):
    # TODO
    pass


def get_teacher_info(username):
    # TODO
    pass


def get_class_info(class_id):
    """
    Provides a dictionary which contains a class':
    class id,
    title,
    teacher suffix,
    teacher username,
    teacher first name,
    teacher surname,
    subject,
    year group,
    section (NULL if there is no assigned section),
    class size
    """


    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()


    sql_query = """
    SELECT classes.title, subjects.subject, teachers.username, teachers.suffix, teachers.first_name, teachers.surname, classes.year_group, classes.section
    FROM classes
    JOIN teachers
    ON classes.teacher = teachers.username
    JOIN subjects
    ON classes.subject_id = subjects.subject_id
    WHERE class_id = ?;
    """

    class_info = cur.execute(sql_query, [class_id]).fetchone()
    print("\n\n\nCLASS INFO", class_info)
    class_info = {
        "id": class_id,
        "title": class_info[0],
        "subject": class_info[1],
        "teacher_username": class_info[2],
        "suffix": class_info[3],
        "teacher_first_name": class_info[4].capitalize(),
        "teacher_surname": class_info[5].capitalize(),
        "year_group": class_info[6],
        "section": class_info[7],
        "class_size": get_class_size(class_id)
    }

    return class_info


def get_class_size(class_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    return cur.execute("SELECT COUNT(*) FROM students_in_classes WHERE class_id = ?", [class_id]).fetchone()[0]


def get_all_subjects():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    subjects = cur.execute("SELECT * FROM subjects").fetchall()

    return subjects


def update_name(f_name, s_name):
    from src.helpers import create_username

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    old_username = session["user_info"]["username"]
    new_username = create_username(f_name, s_name, session["user_info"]["is_student"])

    # update first name, surname, and username 
    if session["user_info"]["is_student"]:
        sql_query = """
        UPDATE students
        SET first_name = ?, surname = ?, username = ?
        WHERE username = ?
        """
    else:
        sql_query = """
        UPDATE teachers
        SET first_name = ?, surname = ?, username = ?
        WHERE username = ?
        """

    cur.execute(sql_query, [f_name, s_name, new_username, old_username])

    # update the session dict
    session["user_info"]["first_name"] = f_name
    session["user_info"]["surname"] = s_name
    session["user_info"]["username"] = new_username


def update_year_group(year_group):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql_query = """
    UPDATE students 
    SET year_group = ?
    WHERE username = ?
    """

    cur.execute(sql_query, [year_group, session["user_info"]["username"]])

    # update the session dict
    session["user_info"]["year_group"] = year_group


def update_section(section):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql_query = """
    UPDATE students 
    SET section = ?
    WHERE username = ?
    """

    cur.execute(sql_query, [section, session["user_info"]["username"]])

    # update the session dict
    session["user_info"]["section"] = section


def update_email(email):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if session["user_info"]["is_student"]:
        sql_query = """
        UPDATE students
        SET email = ?
        WHERE username = ?
        """
    else:
        sql_query = """
        UPDATE teachers
        SET email = ?
        WHERE username = ?
        """
    
    cur.execute(sql_query, [email, session["user_info"]["username"]])

    session["user_info"]["email"] = email


def create_class_db(title, subject_id, year_group, section):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    sql_query = """
    INSERT INTO classes (title, teacher, subject_id, year_group, section) VALUES(?, ?, ?, ?, ?)
    """

    cur.execute(sql_query, [title, session["user_info"]["username"], subject_id, year_group, section])

    con.commit()
    cur.close()