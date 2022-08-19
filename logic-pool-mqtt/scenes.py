import time

DELAY_BETWEEN_POWER_ALERTS = 20

power_alert_counter = 0
last_power_check = 0

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

def powerAlert(homeware, mqtt_client, topic, payload):
  if topic == "device/control":
    if payload["id"] == "current001" and payload["param"] == "brightness":
      global last_power_check
      if time.time() - last_power_check > DELAY_BETWEEN_POWER_ALERTS:
        last_power_check = time.time()
        global power_alert_counter
        power = payload["value"]
        # Power alerts
        if power >= 100:
            power_alert_counter += 1
            homeware.voiceAlert("Sobrecarga de potencia, nivel crítico")
            homeware.execute("scene_power_alert", "deactivate", False)
            mqtt_client.publish("message-alerts", "Sobrecarga de potencia")
        elif power_alert_counter <= 3 and power >= 90:
            power_alert_counter += 1
            homeware.voiceAlert("Sobrecarga de potencia, nivel 9")
            homeware.execute("scene_power_alert", "deactivate", False)
        
        if power_alert_counter >= 1 and power < 75:
            power_alert_counter = 0
            homeware.voiceAlert("Sistemas de potencia bajo control")
            homeware.execute("scene_power_alert", "deactivate", True)

def night(homeware, topic, payload):
  # Day
  if topic == "device/scene_noche/deactivate" and payload:
    color = {
      "spectrumRGB": 16741656,
      "spectrumRgb": 16741656
    }
    homeware.execute("rgb001", "color", color)
  # Night
  elif topic == "device/scene_noche/deactivate" and not payload:
    color = {
      "spectrumRGB": 16729344,
      "spectrumRgb": 16729344
    }
    homeware.execute("rgb001", "color", color)
