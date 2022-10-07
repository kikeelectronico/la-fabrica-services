def green(homeware, topic, payload):
  if topic == "device/control":
    if payload["id"] == "switch003" and payload["param"] == "on":
      status = payload["value"]
      control_ids=["light001", "light002"]
      for control_id in control_ids:
        homeware.execute(control_id, "on", status)
  
  elif topic == "device/switch003/on":
    control_ids=["light001", "light002"]
    for control_id in control_ids:
      homeware.execute(control_id, "on", payload)