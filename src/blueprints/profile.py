from ..student import Student
from ..teacher import Teacher

from flask import Flask, Blueprint, render_template, request, session, flash, redirect

import sqlite3

from src.helpers import login_required
from src.db_helpers import update_name, update_year_group, update_section, update_email

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():

    session["view"]["class_id"] = None

    if request.method == "POST":
        # update profile info
        if request.form.get("new-first-name") and request.form.get("new-surname"):
            new_first_name = request.form.get("new-first-name").lower()
            new_surname = request.form.get("new-surname").lower()
            update_name(new_first_name, new_surname)

        elif request.form.get("new-year-group"):
            new_year_group = request.form.get("new-year-group")
            update_year_group(new_year_group)

        elif request.form.get("new-section"):
            new_section = request.form.get("new-section")
            update_section(new_section)

        elif request.form.get("new-email"):
            new_email = request.form.get("new-email")
            update_email(new_email)
        
        return redirect("/profile")
    else:
        return render_template("profile.html", user_info=session["user_info"])



