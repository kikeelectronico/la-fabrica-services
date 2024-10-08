
def sofa_sensor(homeware, topic, payload):
  if topic == "device/pressure001/occupancy":
    if payload == "OCCUPIED":
      homeware.execute("hue_1", "on", False)
