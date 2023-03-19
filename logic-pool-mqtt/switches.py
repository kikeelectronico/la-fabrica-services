
def bedroom(homeware, topic, payload):
  if topic == "device/hue_sensor_12/on":
    if payload:
      scene_dim = homeware.get("scene_dim","deactivate")
      if scene_dim:
        value = not homeware.get("light001","on")
        homeware.execute("light001","on",value)
      else:
        value = not homeware.get("rgb003","on")
        homeware.execute("rgb003","on",value)
    else:
      homeware.execute("light001","on",False)
      homeware.execute("rgb003","on",False)