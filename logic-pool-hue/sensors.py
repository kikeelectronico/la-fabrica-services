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

def bathroom(service, homeware):
  if service["id"] == "73ef0d76-de9f-4cd1-b460-ec626fbc70fc":
    state = service["motion"]["motion"]
    if state:
      if homeware.get("scene_dim","enable"):
        homeware.execute("hue_sensor_2","on",True)
        homeware.execute("light001","on",False)
      else:
        homeware.execute("light001","on",True)
        homeware.execute("hue_sensor_2","on",False)
    else:
        if not homeware.get("hue_sensor_14", "on"):
          homeware.execute("hue_sensor_2","on",False)
          homeware.execute("light001","on",False)

def hall(service, homeware):
  if service["id"] == "918cdad4-9c5e-40f7-9ef2-e6a64072a2ae":
    state = service["motion"]["motion"]
    if state:
      homeware.execute("hue_7","on",False)
    else:
      homeware.execute("hue_7","on",False)




      