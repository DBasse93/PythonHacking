from frontend import app


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"
