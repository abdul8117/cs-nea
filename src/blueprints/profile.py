# user will have the abiltiy to edit their user info

from flask import Flask, Blueprint, render_template, request, session

import sqlite3

from src.helpers import login_required

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    # TODO allow the ability to edit info

    if request.method == "POST":
        pass
    else:
        return render_template("profile.html", user_info=session["user_info"])



