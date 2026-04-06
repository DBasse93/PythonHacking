import functools

from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, flash, g, make_response, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.db import get_db

bp = Blueprint(name="auth", import_name=__name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        db = get_db()
        error = None

        try:
            valid = validate_email(email)
            email = valid.email  # normalisierte Version
        except EmailNotValidError as e:
            error = str(e)

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            resp = make_response(redirect(url_for("dashboard.home")))

            # 👉 Cookie setzen (z. B. user_id)
            resp.set_cookie(
                "user_id",
                str(user["id"]),
                httponly=True,  # kein JS-Zugriff
                secure=True,  # nur HTTPS
                samesite="Lax",  # CSRF-Schutz
            )
            return resp

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = request.cookies.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("index")))

    # 👉 Cookie löschen
    resp.delete_cookie("user_id")

    return resp


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
