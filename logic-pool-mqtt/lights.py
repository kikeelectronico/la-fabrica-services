import json

def resetEdisonBulb(homeware, topic, payload):
  if topic == "device/hue_11/color":
    if not payload["temperatureK"] == 2200:
        homeware.execute("hue_11","color", { "temperatureK": 2200 })

  if topic == "device/hue_11/brightness":
    if int(payload) > 35:
        homeware.execute("hue_11","brightness", 35)

def mirrorPyramids(homeware, topic, payload):
  if topic == "device/hue_4/brightness":
    if not int(payload) == homeware.get("hue_5", "brightness"):
      homeware.execute("hue_5", "brightness", int(payload))

  if topic == "device/hue_5/brightness":
    if not int(payload) == homeware.get("hue_4", "brightness"):
      homeware.execute("hue_4", "brightness", int(payload))