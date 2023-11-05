from datetime import datetime

def bedroom(service, homeware):
  if service["id"] == "f3a99b17-a6cb-4b51-9da6-c9a90b1eda65":
    state = service["motion"]["motion"]
    if state:
      if homeware.get("scene_dim","enable"):
        homeware.execute("rgb003","on",True)
        homeware.execute("hue_6","on",False)
      else:
        homeware.execute("hue_6","on",True)
        homeware.execute("rgb003","on",False)
    else:
        if not homeware.get("hue_sensor_12", "on"):
          homeware.execute("hue_6","on",False)
          homeware.execute("rgb003","on",False)




      