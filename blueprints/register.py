from flask import Blueprint, request, redirect, render_template

from helpers import login_required

register_blueprint = Blueprint("register", __name__)

@register_blueprint.route("/register", methods=["GET", "POST"])
def register():

    """
    This function is called when a user visits the /register route.
    If the user is simply visiting the site, it is a GET request and the 'else' block of the selection below is executed.
    If the user had submitted a form, then a POST request is sent to the server where the form input will be handled.
    """


    if request.method == "POST":

        first_name = request.form.get("first_name").lower().strip()
        surname = request.form.get("surname").lower().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        
        if request.form.get("account_type") == "student":
            is_student = True
            year_group = request.form.get("year-group")
            section = request.form.get("section")
        else:
            is_student = False
            suffix = request.form.get("suffix")
        
        # First and surnames can only be one word and completely alphabetical
        if not(first_name and surname):
            # checks if the name fields are not left blank
            print("Name(s) not given")
            return redirect("/register")
        elif not(first_name.isalpha() and surname.isalpha()):
            print("Name(s) must be completely alphabteical")
            return redirect("/register")
        elif len(first_name.split()) != 1 or len(surname.split()) != 1:
            print("Name(s) must be only one word")
            return redirect("/register")
        
        # email
        if not(email):
            print("Email not given")
        # TODO Validate email(?)

        # both password fields must be given
        if not(password and confirm_password):
            redirect("/register")
        elif password != confirm_password:
            print("Passwords do not match")
            return redirect("/register")
        
        # make sure the account type and year group was selected
        # if not(account_type):
            # print("Account type must be given")
            # redirect("/register")
        # if not(year_group):
        #     print("Year group must be given")
        #     redirect("/register")
        
          
        # Create username
        username = create_username(first_name, surname, is_student)
        
        # Hash password using a salt, then encrypt it
        # salt = generate_salt()
        # hash_with_salt = hash(password + salt)
        # key = generate_key(len(str(hash_with_salt)))
        # encrypted_hash = vernam_cipher.encrypt(hash_with_salt, key)

        password = security.generate_password_hash(password)

        # Insert into DB
        if is_student:
            details = (username, first_name, surname, email, password, year_group, section)
        else:
            details = (username, first_name, surname, suffix, email, password)
        insert_user_to_database(details, is_student)

        if is_student: 
            session["user_info"] = {
                "username": username,
                "first_name": first_name,
                "surname": surname,
                "email": email,
                "year_group": year_group,
                "section": section,
                "is_student": is_student
            }
        else:
            session["user_info"] = {
                "username": username,
                "first_name": first_name,
                "surname": surname,
                "suffix": suffix,
                "email": email,
                "is_student": is_student
            }
            

        return redirect("/")

    else:
        # Page accessed via a GET request
        return render_template("register.html")
