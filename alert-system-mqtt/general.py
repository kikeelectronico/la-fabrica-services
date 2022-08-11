import json

from homeware import Homeware
from Voice import Voice

voice = Voice()
homeware = Homeware()

store = {}
power_alert_counter = 0

def power(topic, payload):
  if topic == "device/control":
    payload = json.loads(payload)
    if payload["id"] == "switch003" and payload["param"] == "on":
        voice.getAndPlay("Alguien ha usado en interruptor de internet")
    if payload["id"] == "current001" and payload["param"] == "brightness":
        power = payload["value"]
        global store
        global power_alert_counter
        # Power alerts
        if power >= 90:
            # Get home devices status
            devices = homeware.getDevices()
            store["rgb001"] = {
                "color": devices["rgb001"]["color"],
                "on": devices["rgb001"]["on"]
            }
            color = {
                "spectrumRGB": 16711680,
                "spectrumRgb": 16711680
            }
            homeware.setParam("rgb001", "color", color)
            homeware.setParam("rgb001", "on", True)

        if power >= 100:
            power_alert_counter += 1
            voice.getAndPlay("Sobrecarga de potencia, nivel crítico")
        elif power_alert_counter <= 3 and power >= 90:
            power_alert_counter += 1
            voice.getAndPlay("Sobrecarga de potencia, nivel 9")
        
        if power_alert_counter >= 1 and power < 75:
            power_alert_counter = 0
            voice.getAndPlay("Sistemas de potencia bajo control")
            homeware.setParam("rgb001", "color", store["rgb001"]["color"])
            homeware.setParam("rgb001", "on", store["rgb001"]["on"])

def checkSystemsByVoice(topic, payload):
  if topic == "home" and payload == "check_systems_by_voice":
    voice.getAndPlay("Hola Enrique, todos los sistemas están operativos")