from flask import redirect, url_for, session

from functools import wraps

# def login_required(f):
#     """
#     https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/    
#     """

#     @wraps(f)
#     def dec_function():
#         if not(session.get("user_info")):
#             # User is not logged in
#             return redirect("/login")
#         # User is logged in
#         return f(*args, **kwargs)

#     return dec_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info = session.get("user_info")
        print("user info",user_info)
        if user_info is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def generate_salt():
    """
    https://docs.python.org/3/library/secrets.html
    """

    from secrets import choice
    from string import ascii_letters

    salt = ""
    length = choice(list(range(10, 21)))
    indexes = [x for x in range(len(ascii_letters))]

    # "".join(ascii_letters[choice(indexes)] for x in range(len(length)))

    for i in range(length):
        index = choice(indexes)
        salt += ascii_letters[choice(indexes)]
    
    return salt


def generate_key(length):
    from secrets import choice
    from string import ascii_letters

    key = ""
    indexes = [x for x in range(len(ascii_letters))]

    # "".join(ascii_letters[choice(indexes)] for x in range(len(length)))

    for i in range(length):
        key += ascii_letters[choice(indexes)]
    
    return key


def create_username(f_name, s_name, is_student):
    """
    Students:
    firstname + '.' + first letter of their surname + '_s'

    Teachers:
    first letter of their first name + '.' surname + '_t'
    """

    if is_student:
        return f_name + "." + s_name[0] + "_s"
    else:
        return f_name[0] + "." + s_name + "_t"


def insert_user_into_database(details, is_student):
    import sqlite3

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    if is_student:
        cur.execute("INSERT INTO students (username, first_name, surname, year_group, section, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", details)
    else:
        cur.execute("INSERT INTO teachers (username, first_name, surname, suffix, email, password, salt) VALUES (?, ?, ?, ?, ?, ?, ?)", details)
    con.commit()
    con.close()
