
def main(homeware, topic, payload):
  whitelist = [
    "device/scene_table_sensor/enable"
  ]

  if topic in whitelist :
    table_sensor = homeware.get("scene_tablet_sensor", "enable")
    if table_sensor:
      homeware.execute("scene_work", "enable", True)
    else:
      homeware.execute("scene_work", "enable", False)

