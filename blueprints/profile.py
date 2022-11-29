# user will have the abiltiy to edit their user info

from flask import Flask, Blueprint, render_template, request, session

import sqlite3

from helpers import login_required

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods=["GET", "POST"])
def profile_page():
    # TODO allow the ability to edit info
    
    return render_template("profile.html", user_info=session["user_info"])
