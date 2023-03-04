from flask import redirect, url_for, session

from functools import wraps

def login_required(f):
    # https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    # This function is adapted from the documentation above. It is used to check if a user is logged in before allowing them to access a page.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info = session.get("user_info")
        # print("user info",user_info)
        if user_info is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function

# The two functions below are used to check if a user is a student or a teacher before allowing them to access a page. If they are not, unauthorised.html is returned.
def only_students(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info = session.get("user_info")
        # print("user info",user_info)
        if not user_info["is_student"]:
            return redirect(url_for("unauthorised"))
        return f(*args, **kwargs)

    return decorated_function

def only_teachers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info = session.get("user_info")
        # print("user info",user_info)
        if user_info["is_student"]:
            return redirect(url_for("unauthorised"))
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

    # TODO logic for if a username is a duplicate

    if is_student:
        return f_name + "." + s_name[0] + "_s"
    else:
        return f_name[0] + "." + s_name + "_t"
