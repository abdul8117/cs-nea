from flask import redirect, session

from functools import wraps

def login_required(f):
    """
    https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash
    """

    @wraps(f)
    def dec_function():
        if not(session.get("user_info")):
            # User is not logged in
            return redirect("/login")
        
        # User is logged in
        return f()
    
    return dec_function


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


def create_username(f_name, s_name, type):
    """
    Students:
    firstname + '.' + first letter of their surname + '_s'

    Teachers:
    first letter of their first name + '.' surname + '_t'
    """

    if type == "student":
        return f_name + "." + s_name[0] + "_s"
    else:
        return f_name[0] + "." + s_name + "_t"


def insert_user_to_database(details, account_type):
    """
    TODO info
    """

    import sqlite3

    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    if account_type == "student":
        cur.execute("INSERT INTO students (username, email, first_name, surname, password, year_group) VALUES (?, ?, ?, ?, ?, ?)", details)
    else:
        cur.execute("INSERT INTO teachers (username, email, first_name, surname, password, year_group) VALUES (?, ?, ?, ?, ?, ?)", details)
    con.commit()
    con.close()
