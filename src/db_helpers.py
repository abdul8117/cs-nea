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


def get_class_info(class_id):
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

    class_info["class_size"] = get_class_size(class_id)

    return class_info


def get_class_size(class_id):
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()

    return cur.execute("SELECT COUNT(*) FROM students_in_classes WHERE class_id = ?", [class_id]).fetchone()[0]