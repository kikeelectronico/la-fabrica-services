import imp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.cloud.logging as logging
import os
from spotify import Spotify
from weather import Weather
from homeware import Homeware
from launches import Launches
from internet import Internet

# Load env vars
if os.environ.get("ENV", "dev") == "dev":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

ENV = os.environ.get("ENV", "dev")

# Define constants
SERVICE = "data-panel-api-" + ENV

# Instantiate objects
app = FastAPI()
logger = logging.Client().logger(SERVICE)
logger.log_text("Starting", severity="INFO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

spotify = Spotify()
weatherapi = Weather()
homeware = Homeware()
launchesapi = Launches()
internet = Internet()

@app.get("/")
async def root():
  return {"message": "Hello, World!"}

@app.get("/spotify")
async def spotifyEndPoint():
  playing = spotify.getPlaying(logger, max_tries=2)
  return playing

@app.get("/weather")
async def weatherEndPoint():
  (fail_to_update, weather_flag, weather) = weatherapi.getWeather()

  return {
    "fail_to_update": fail_to_update,
    "weather_flag": weather_flag,
    "weather": weather
  }

@app.get("/homeware")
async def homewareEndPoint():
  (status_flag, status) = homeware.getStatus()
  #(devices_flag, devices) = homeware.getDevices()

  return {
    "status_flag": status_flag,
    #"devices_flag": devices_flag,
    "status": status,
    #"devices": devices,
  }

@app.get("/launches")
async def launchesEndPoint():
  (fail_to_update, launches_flag, launches) = launchesapi.getLaunches()

  return {
    "fail_to_update": fail_to_update,
    "launches_flag": launches_flag,
    "launches": launches
  }

@app.get("/internet")
async def internetEndPoint():
  connectivity = internet.checkConnectivity()
  return connectivity

@app.get("/alerts")
async def alertsEndPoint():
  (fail_to_update, weather_flag, weather) = weatherapi.getWeather()

  alerts = []

  # Forecast
  forecast = weather['forecast']['forecastday']

  for (i, day) in enumerate(forecast):
    if day['day']['daily_will_it_rain'] == 1 and i == 0:
      alerts.append({
        "text": "Hoy llueve",
        "severity": "normal",
        "image": "cloud.png"
      })
    elif day['day']['daily_will_it_rain'] == 1 and i == 1:
      alerts.append({
        "text": "Mañana va a llover",
        "severity": "normal",
        "image": "cloud.png"
      })

  return alerts