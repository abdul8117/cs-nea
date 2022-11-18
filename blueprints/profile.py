# user will have the abiltiy to edit their user info

from flask import Flask, Blueprint, render_template, request
from flask_session import Session

import sqlite3

from helpers import login_required

profile_bp = Blueprint("profile", __name__)

profile = Flask(__name__)
profile.config["SESSION_PERMANENT"] = False
profile.config["SESSION_TYPE"] = "filesystem"
profile.config["SESSION_COOKIE_PATH"] = "/"
Session(profile)

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    # TODO allow the ability to edit info
    
    return render_template("profile.html", user_info=session["user_info"])
