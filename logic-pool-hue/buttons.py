import json

long_pressing = False

def bedroom(id, state, homeware):
    global long_pressing
    if id == "12":
      if state["buttonevent"] == 1001:
          if not long_pressing:
            value = not homeware.get("scene_dim","enable")
            homeware.execute("scene_dim","enable",value)
            long_pressing = True

      elif state["buttonevent"] == 1003:
          long_pressing = False

      elif state["buttonevent"] == 1002:
          value = not homeware.get("hue_sensor_12","on")
          homeware.execute("hue_sensor_12","on",value)

def kitchen(id, state, homeware):
    global long_pressing
    if id == "13":
      if state["buttonevent"] == 1002:
          value = not homeware.get("light004","on")
          homeware.execute("light004","on",value)

def bathroom(id, state, homeware):
    global long_pressing
    if id == "14":
      if state["buttonevent"] == 1001:
          if not long_pressing:
            value = not homeware.get("scene_dim","enable")
            homeware.execute("scene_dim","enable",value)
            long_pressing = True

      elif state["buttonevent"] == 1003:
          long_pressing = False

      elif state["buttonevent"] == 1002:
          value = not homeware.get("hue_sensor_14","on")
          homeware.execute("hue_sensor_14","on",value)
      
             