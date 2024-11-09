LIVINGROOM_LIGHT_THRESHOLD = 20

def livingroomLight(homeware, topic, payload):
  if topic == "device/c8bd20a2-69a5-4946-b6d6-3423b560ffa9/brightness":
    if int(payload) > LIVINGROOM_LIGHT_THRESHOLD:
      if homeware.get("scene_dim", "enable"):
        homeware.execute("scene_dim", "enable", False)