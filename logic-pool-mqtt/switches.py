
def bedroom(homeware, topic, payload):
  if topic == "device/hue_sensor_12/on":
    if payload:
      if homeware.get("scene_dim","enable"):
        value = not homeware.get("rgb003","on")
        homeware.execute("rgb003","on",value)
        homeware.execute("hue_6","on",False)
      else:
        value = not homeware.get("hue_6","on")
        homeware.execute("hue_6","on",value)
        homeware.execute("rgb003","on",False)
    else:
      homeware.execute("hue_6","on",False)
      homeware.execute("rgb003","on",False)

def livingroom(homeware, topic, payload):
  if topic == "device/switch_temp_1/on":
    if payload:
      if homeware.get("scene_dim","enable"):
        homeware.execute("hue_4","on",False)
        homeware.execute("hue_5","on",False)
        homeware.execute("rgb001","on",True)
        homeware.execute("rgb002","on",True)
        homeware.execute("hue_1","on",True)
        homeware.execute("light003","on",True)
        #homeware.execute("light004","on",False)
      else:
        homeware.execute("hue_4","on",True)
        homeware.execute("hue_5","on",True)
        homeware.execute("rgb001","on",True)
        homeware.execute("rgb002","on",True)
        homeware.execute("hue_1","on",False)
        homeware.execute("light003","on",False)
    else:
      homeware.execute("hue_4","on",False)
      homeware.execute("hue_5","on",False)
      homeware.execute("rgb001","on",False)
      homeware.execute("rgb002","on",False)
      homeware.execute("hue_1","on",False)
      homeware.execute("light003","on",False)

def kitchen(homeware, topic, payload):
  if topic == "device/hue_sensor_13/on":
    if payload:
      homeware.execute("light004","on",True)
    else:
      homeware.execute("light004","on",False)

def mirror(homeware, topic, payload):
  if topic == "device/hue_sensor_2/on":
    if payload:
      homeware.execute("hue_2","on",True)
      homeware.execute("hue_3","on",True)
    else:
      homeware.execute("hue_2","on",False)
      homeware.execute("hue_3","on",False)