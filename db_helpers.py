import sqlite3

def insert_user_into_database(details, is_student):
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    if is_student:
        cur.execute("INSERT INTO students (username, first_name, surname, year_group, section, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", details)
    else:
        cur.execute("INSERT INTO teachers (username, first_name, surname, suffix, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?)", details)
    con.commit()
    con.close()


def get_subject_from_id(id):
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    subject = cur.execute("SELECT subject FROM subjects WHERE subject_id = ?", [id]).fetchone()[0]

    return subject

def get_teacher_name(username):
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    teacher_name = cur.execute("SELECT first_name, surname FROM teachers WHERE username = ?", [username]).fetchall()[0]
    print(teacher_name)

    return teacher_name