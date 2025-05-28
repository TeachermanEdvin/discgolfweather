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
        f"&start_date={date}&end_date={date}&timezone=Europe%2FStockholm"
    )

    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    forecast = []

    for idx, timestamp in enumerate(times):
        hour_str = timestamp.split("T")[-1][:5]  # Extract HH:MM
        if "08:00" <= hour_str <= "20:00":
            wind_kmh = data["hourly"]["windspeed_10m"][idx]
            wind_ms = round(wind_kmh / 3.6, 1)
            forecast.append({
                "time": hour_str,
                "temperature": data["hourly"]["temperature_2m"][idx],
                "precipitation": data["hourly"]["precipitation"][idx],
                "wind": wind_ms
            })

    return forecast

def calculate_score(forecast):
    score = 0
    for f in forecast:
        temp_diff = abs(f["temperature"] - 15)
        score += (10 - min(temp_diff, 10))  # max 10 poäng
        score += max(0, 5 - f["precipitation"])  # max 5 poäng
        score += max(0, 5 - f["wind"])  # max 5 poäng
    return round(score / len(forecast), 1) if forecast else 0

@app.route("/", methods=["GET", "POST"])
def index():
    date = "2025-05-30"
    weather_data = {}
    if request.method == "POST":
        for city in ["Falun", "Nyköping"]:
            forecast = get_weather(city, date)
            score = calculate_score(forecast)
            weather_data[city] = {
                "forecast": forecast,
                "score": score
            }
        return render_template("index.html", weather=weather_data)
    return render_template("index.html", weather=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
