from flask import Blueprint, request, session, redirect, render_template

auth = Blueprint("auth", __name__)

USERNAME = "admin"
PASSWORD = "1234"

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form.get("username") == USERNAME
            and request.form.get("password") == PASSWORD
        ):
            session["logged_in"] = True
            return redirect("/shifts")
    return render_template("login.html")

from functools import wraps
from flask import session, redirect

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/")
        return fn(*args, **kwargs)
    return wrapper

