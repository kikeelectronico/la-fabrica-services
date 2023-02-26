# Propagate color changes on RGB strips
def rgbPropagation(homeware, topic, payload):
  if topic == "device/rgb001/color":
    control_ids = ["rgb002"]
    for control_id in control_ids:
      homeware.execute(control_id, "color", payload)
  if topic == "device/rgb001/on":
    control_ids = ["rgb002"]
    for control_id in control_ids:
      homeware.execute(control_id, "on", payload)