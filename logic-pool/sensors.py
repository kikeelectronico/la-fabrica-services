
def livingroom(homeware, topic, payload):
  if topic == "device/c8bd20a2-69a5-4946-b6d6-3423b560ffa9/brightness":
    if not homeware.get("scene_dim", "enable"):
      # if int(payload) > 20:
        # homeware.execute("scene_dim", "eneable", False)
      brightness = int((int(payload) * 1.4) + 20)
      if not homeware.get("hue_sensor_12", "on"):
        homeware.execute("hue_6", "brightness", brightness)
      homeware.execute("hue_7", "brightness", brightness)
      # else:
      #   homeware.execute("scene_dim", "eneable", True)

def sofa(homeware, topic, payload):
  if topic == "device/pressure001/occupancy":
    if payload == "OCCUPIED":
      homeware.execute("hue_9", "on", False)
      homeware.execute("hue_10", "on", False)

def bedroom(homeware, topic, payload):
  if topic == "device/pressure002/occupancy":
    if payload == "OCCUPIED":
      homeware.execute("scene_sensors_enable", "enable", False)  
      homeware.execute("scene_dim", "enable", True)      
    elif payload == "UNOCCUPIED":
      homeware.execute("scene_sensors_enable", "enable", True)
      if homeware.get("scene_astro_day","enable"):
        homeware.execute("scene_dim", "enable", False)