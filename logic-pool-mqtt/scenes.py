import time

DELAY_BETWEEN_POWER_ALERTS = 30

power_alert_counter = 0
last_power_check = 0
waiting_for_shower = False

def film(homeware, topic, payload):
  if topic == "device/scene_pelicula/deactivate" and not payload:
    # Turn off some lights
    turn_off_devices = ["light001", "light002", "light003", "light004", "hue_1"]
    for control_id in turn_off_devices:
      homeware.execute(control_id, "on", False)
    # Change the color of some lights
    color = {
      "spectrumRGB": 16741656,
      "spectrumRgb": 16741656
    }
    homeware.execute("rgb001", "color", color)
    homeware.execute("rgb002", "color", color)
    # Turn on some lights
    turn_on_devices = ["rgb001", "rgb002"]
    for control_id in turn_on_devices:
      homeware.execute(control_id, "on", True)
    homeware.execute("scene_pelicula", "deactivate", True)

def shower(homeware, alert, topic, payload):
  global waiting_for_shower
  if topic == "device/scene_ducha/deactivate" and not payload:
    homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 27)
    homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
    waiting_for_shower = True
  elif topic == "device/scene_ducha/deactivate" and payload:
    homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
    waiting_for_shower = False

  if topic == "device/thermostat_bathroom" and waiting_for_shower:
    if payload["thermostatTemperatureAmbient"] >= payload["thermostatTemperatureSetpoint"]:
      alert.voice("disfruta de la ducha", gpt3=True)
      waiting_for_shower = False

def relax(homeware, topic, payload):
  if topic == "device/scene_relajacion/deactivate" and not payload:
    turn_on_devices = ["light003", "rgb001", "rgb002", "rgb003"]
    for control_id in turn_on_devices:
      homeware.execute(control_id, "on", True)
    turn_off_devices = ["light001", "light002", "light004", "hue_1"]
    for control_id in turn_off_devices:
      homeware.execute(control_id, "on", False)
    homeware.execute("scene_relajacion", "deactivate", True)

def powerAlert(homeware, alert, topic, payload):
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
          if power_alert_counter > 1:
            alert.voice("Sobrecarga de potencia, nivel crítico")
            alert.message("Sobrecarga de potencia")
            currentToggleSettings = {
              "emergencia": True
            }
            homeware.execute("rgb001", "currentToggleSettings", currentToggleSettings)
            homeware.execute("rgb002", "currentToggleSettings", currentToggleSettings)
            homeware.execute("rgb003", "currentToggleSettings", currentToggleSettings)
        # elif power_alert_counter <= 3 and power >= 90:
        #   power_alert_counter += 1
        #   homeware.voiceAlert("Sobrecarga de potencia, nivel 9")
        if power < 85:
          if power_alert_counter > 1:
            power_alert_counter = 0
            alert.voice("Sistemas de potencia bajo control")
            currentToggleSettings = {
              "emergencia": False
            }
            homeware.execute("rgb001", "currentToggleSettings", currentToggleSettings)
            homeware.execute("rgb002", "currentToggleSettings", currentToggleSettings)
            homeware.execute("rgb003", "currentToggleSettings", currentToggleSettings)
          
          if power_alert_counter == 1:
            power_alert_counter = 0

def night(homeware, topic, payload):
  # Day
  if topic == "device/scene_noche/deactivate" and payload:
    color = {
      "spectrumRGB": 16741656,
      "spectrumRgb": 16741656
    }
    homeware.execute("rgb001", "color", color)
    homeware.execute("rgb003", "color", color)
  # Night
  elif topic == "device/scene_noche/deactivate" and not payload:
    color = {
      "spectrumRGB": 16729344,
      "spectrumRgb": 16729344
    }
    homeware.execute("rgb001", "color", color)
    homeware.execute("rgb003", "color", color)
    homeware.execute("thermostat_bedroom", "thermostatTemperatureSetpoint", 19)
