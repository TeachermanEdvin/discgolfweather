from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def get_weather(city, date):
    lat_lon = {
        "Falun": (60.606, 15.633),
        "Nyköping": (58.753, 17.007)
    }
    lat, lon = lat_lon[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&start_date={date}&end_date={date}&timezone=Europe%2FBerlin"
    response = requests.get(url)
    data = response.json()

    if "daily" in data:
        return {
            "max_temp": data["daily"]["temperature_2m_max"][0],
            "min_temp": data["daily"]["temperature_2m_min"][0],
            "precipitation": data["daily"]["precipitation_sum"][0]
        }
    else:
        return None

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
    app.run(debug=True)
