
def sofa_sensor(homeware, topic, payload):
  if topic == "device/sensor_001/on":
    if payload:
      homeware.execute("hue_1", "on", False)
