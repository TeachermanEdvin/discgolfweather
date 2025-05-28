# app.py
from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

def get_weather(city, date):
    lat_lon = {
        "Falun": (60.606, 15.633),
        "Nyköping": (58.753, 17.007)
    }
    lat, lon = lat_lon[city]

    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation,windspeed_10m"
        f"&start_date={date}&end_date={date}&timezone=Europe%2FBerlin"
    )

    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    target_hours = ["08:00", "12:00", "15:00", "18:00"]

    forecast = []
    for target in target_hours:
        datetime_str = f"{date}T{target}"
        if datetime_str in times:
            idx = times.index(datetime_str)
            forecast.append({
                "time": target,
                "temperature": data["hourly"]["temperature_2m"][idx],
                "precipitation": data["hourly"]["precipitation"][idx],
                "wind": data["hourly"]["windspeed_10m"][idx]
            })

    return forecast

@app.route("/", methods=["GET", "POST"])
def index():
    date = "2025-05-30"
    weather_data = {}
    if request.method == "POST":
        for city in ["Falun", "Nyköping"]:
            weather_data[city] = get_weather(city, date)
        return render_template("index.html", weather=weather_data)
    return render_template("index.html", weather=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
