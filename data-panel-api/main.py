import imp
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from spotify import Spotify
from weather import Weather
from homeware import Homeware
from launches import Launches
from internet import Internet
from logger import Logger

# Load env vars
if os.environ.get("ENV", "dev") == "dev":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
MQTT_PORT = 1883
ENV = os.environ.get("ENV", "dev")

# Define constants
SERVICE = "data-panel-api-" + ENV

# Instantiate objects
app = FastAPI()
mqtt_client = mqtt.Client(client_id=SERVICE) 
logger = Logger(mqtt_client, SERVICE)

# Check env vars
def report(message):
  print(message)
  #logger.log(message, severity="ERROR")
  exit()
if MQTT_USER == "no_set":
  report("MQTT_USER env vars no set")
if MQTT_PASS == "no_set":
  report("MQTT_PASS env vars no set")
if MQTT_HOST == "no_set":
  report("MQTT_HOST env vars no set")

 # Connect to the mqtt broker
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
logger.log("Starting " + SERVICE , severity="INFO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

spotify = Spotify(logger)
weatherapi = Weather(logger)
homeware = Homeware(logger)
launchesapi = Launches(logger)
internet = Internet(logger)

@app.get("/")
async def root():
  return {"message": "Hello, World!"}

@app.get("/spotify")
async def spotifyEndPoint():
  playing = spotify.getPlaying(max_tries=2)
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
  alerts = []

  # Forecast
  (fail_to_update, weather_flag, weather) = weatherapi.getWeather()
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

  # Home alerts      
  (status_flag, status) = homeware.getStatus()
  humidity = status["thermostat_livingroom"]["thermostatHumidityAmbient"]
  if humidity < 30:
    alerts.append({
      "text": "Humedad baja",
      "severity": "normal",
      "image": "drops.png"
    })
  elif humidity > 60:
    alerts.append({
      "text": "Humedad alta",
      "severity": "normal",
      "image": "drops.png"
    })

  return alerts

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )