from datetime import datetime

MOTION_TIMER = 60

last_report_checked = {
  "bedroom": 0
}

def bedroom(id, state, homeware):
  if id == "c2b38173-883e-4766-bcb5-0cce2dc0e00e":
    if state["motion"]:
      if not last_report_checked["bedroom"] == state["motion_report"]["changed"]:
        if homeware.get("scene_dim","enable"):
          homeware.execute("rgb003","on",True)
          homeware.execute("hue_6","on",False)
        else:
          homeware.execute("hue_6","on",True)
          homeware.execute("rgb003","on",False)
        last_report_checked["bedroom"] = state["motion_report"]["changed"]
    else:
        if not homeware.get("hue_sensor_12", "on"):
          last_report_string = state["motion_report"]["changed"]
          last_report_string = last_report_string.replace("Z", "UTC")
          last_report = datetime.strptime(last_report_string, "%Y-%m-%dT%H:%M:%S.%f%Z")
          now = datetime.utcnow()
          delta = now - last_report
          delta_seconds = delta.total_seconds()
          if delta_seconds > MOTION_TIMER:
            homeware.execute("hue_6","on",False)
            homeware.execute("rgb003","on",False)




      