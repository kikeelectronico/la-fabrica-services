import json

def resetEdisonBulb(homeware, topic, payload):
  if topic == "device/hue_11/color":
    if not payload["temperatureK"] == 2200:
        homeware.execute("hue_11","color", { "temperatureK": 2200 })

  if topic == "device/hue_11/brightness":
    if payload > 35:
        homeware.execute("hue_11","brightness", 35)
