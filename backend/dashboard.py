import requests
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from backend.auth import login_required
from backend.db import get_db

bp = Blueprint(name="dashboard", import_name=__name__, url_prefix="/dashboard")


@bp.route("/home", methods=("GET", "POST"))
@login_required
def home():
    lat = 52.37
    lon = 9.72
    weather = {}

    if request.method == "POST":
        lat = request.form.get("latitude", type=float)
        lon = request.form.get("longitude", type=float)

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current_weather", {})
    except requests.RequestException as e:
        print("Fehler beim Abrufen der Wetterdaten:", e)

    return render_template(
        "dashboard/home.html",
        latitude=lat,
        longitude=lon,
        temperature=weather.get("temperature"),
        windspeed=weather.get("windspeed"),
        weathercode=weather.get("weathercode"),
        time=weather.get("time"),
    )


@bp.route("/weather", methods=("GET", "POST"))
@login_required
def weather():
    db = get_db()
    rows = db.execute("SELECT * FROM weather ORDER BY time DESC").fetchall()

    flash("Wetterdaten erfolgreich abgerufen ✅")
    return render_template("dashboard/weather.html", weather_list=rows)


@bp.route("/save_weather", methods=("POST",))
@login_required
def save_weather():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    temperature = request.form.get("temperature")
    windspeed = request.form.get("windspeed")
    weathercode = request.form.get("weathercode")
    time = request.form.get("time")

    if not latitude or not longitude:
        flash("Latitude und Longitude müssen angegeben werden.")
        return redirect(url_for("dashboard.home"))

    db = get_db()
    db.execute(
        "INSERT INTO weather (user_id, latitude, longitude, temperature, windspeed, weathercode, time) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (g.user["id"], latitude, longitude, temperature, windspeed, weathercode, time),
    )
    db.commit()
    flash("Wetterdaten erfolgreich gespeichert ✅")
    return redirect(url_for("dashboard.home"))
