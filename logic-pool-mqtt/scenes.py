def film(homeware, topic, payload):
  if topic == "device/scene_pelicula/deactivate" and not payload:
    turn_off_devices = ["light001", "light002", "light003", "outlet001", "rgb001"]
    for control_id in turn_off_devices:
      homeware.execute(control_id, "on", False)
    homeware.execute("scene_pelicula", "deactivate", True)

def relax(homeware, topic, payload):
  if topic == "device/scene_relajacion/deactivate" and not payload:
    turn_on_devices = ["light003", "rgb001", "rgb002", "rgb001"]
    for control_id in turn_on_devices:
      homeware.execute(control_id, "on", True)
    turn_off_devices = ["light001", "light002", "outlet001"]
    for control_id in turn_off_devices:
      homeware.execute(control_id, "on", False)
    homeware.execute("scene_relajacion", "deactivate", True)