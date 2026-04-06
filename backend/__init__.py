"""
Package app __init__.

Detailed description:
   ...
"""

import os

# from flask import Flask, redirect, render_template, request, url_for
# from flask.typing import ResponseReturnValue
from flask import Flask


def create_app(test_config: None = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route("/hello")
    def hello() -> str:
        return "Hello, World!"

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app


# @app.route("/")
# def home() -> ResponseReturnValue:
#     return render_template("home.html")


# @app.route("/login", methods=["GET", "POST"])
# def login() -> ResponseReturnValue:
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             print(f"{theuser},{thepass}")
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)


# @app.route("/register", methods=["GET", "POST"])
# def register() -> ResponseReturnValue:
#     if request.method == "POST":
#         theuser = request.form.get("username")
#         theemail = request.form.get("email")
#         thepass1 = request.form.get("password1")
#         thepass2 = request.form.get("password2")
#         print(f"{theuser},{theemail},{thepass1},{thepass2}")

#         return redirect(url_for("register"))
#     return render_template("register.html")


# @app.route("/tickets")
# def tickets() -> ResponseReturnValue:
#     dbitems = [
#         {"id": 1, "priority": 2, "username": "Mark", "title": "something broken"},
#         {"id": 2, "priority": 1, "username": "Natalie", "title": "nothing to do"},
#         {"id": 3, "priority": 3, "username": "Luke", "title": "looks not good"},
#     ]
#     return render_template("tickets.html", items=dbitems)
