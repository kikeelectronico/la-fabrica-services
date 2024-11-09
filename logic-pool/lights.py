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

  if topic == "device/hue_4/color":
    if not payload["temperatureK"] == homeware.get("hue_5", "color")["temperatureK"]:
      homeware.execute("hue_5", "color", payload)

  if topic == "device/hue_5/color":
    if not payload["temperatureK"] == homeware.get("hue_4", "color")["temperatureK"]:
      homeware.execute("hue_4", "color", payload)

MIN_LIVINGROOM_DARKNESS_TRIGGER = 20

def sofaLight(homeware, topic, payload):
  if topic == "device/c8bd20a2-69a5-4946-b6d6-3423b560ffa9/brightness" or topic == "device/pressure001/occupancy":
    if payload == "OCCUPIED":
      homeware.execute("hue_1", "on", False)
    else:
      light_level = int(payload) if topic == "device/c8bd20a2-69a5-4946-b6d6-3423b560ffa9/brightness" else homeware.get("c8bd20a2-69a5-4946-b6d6-3423b560ffa9", "brightness")
      occupancy = payload if topic == "device/pressure001/occupancy" else homeware.get("pressure001", "occupancy")
      if light_level < MIN_LIVINGROOM_DARKNESS_TRIGGER and homeware.get("scene_awake", "enable") and occupancy == "UNOCCUPIED":
        homeware.execute("hue_1", "on", True)
      elif light_level >= MIN_LIVINGROOM_DARKNESS_TRIGGER and homeware.get("scene_awake", "enable") and occupancy == "UNOCCUPIED":
        homeware.execute("hue_1", "on", False)