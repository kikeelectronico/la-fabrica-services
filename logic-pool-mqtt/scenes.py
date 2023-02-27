import time

DELAY_BETWEEN_POWER_ALERTS = 30

power_alert_counter = 0
last_power_check = 0
waiting_for_shower = False

scene_pre_state = {}

# Set the film scene
def film(homeware, alert, topic, payload):
  if topic == "device/scene_pelicula/deactivate":
    global scene_pre_state
    if not payload:
      # Activate scene
      alert.voice("¡me encantan las películas!", speaker="livingroom", gpt3=True)
      # Save current status
      devices_id = ["light001", "light002", "light003", "light004", "hue_1", "rgb001", "rgb002"]
      for device_id in devices_id:
        scene_pre_state[device_id] = homeware.get(device_id, "all")
      # Turn off some lights
      turn_off_devices = ["light001", "light002", "light003", "light004", "hue_1"]
      for control_id in turn_off_devices:
        homeware.execute(control_id, "on", False)
      # Change the color of some lights and turn them on
      turn_on_devices = ["rgb001", "rgb002"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      # Change color
      for control_id in turn_on_devices:
        homeware.execute(control_id, "color", color)
      # Turn on
      for control_id in turn_on_devices:
        homeware.execute(control_id, "on", True)
    else:
      # Deactivate scene
      devices_id = ["light001", "light002", "light003", "light004", "hue_1", "rgb001", "rgb002"]
      for device_id in devices_id:
        device_state = scene_pre_state[device_id]
        for param in device_state:
          homeware.execute(device_id, param, device_state[param])

# Set the shower scene
def shower(homeware, alert, topic, payload):
  global waiting_for_shower
  if topic == "device/scene_ducha/deactivate" and not payload:
    # Start preparing the bathroom
    alert.voice("voy a preparar el baño para que te duches.", gpt3=True)
    homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 27)
    homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
    waiting_for_shower = True
  elif topic == "device/scene_ducha/deactivate" and payload:
    # Return the bathroom to normal
    alert.voice("espero que te hayas disfrutado de la ducha.", gpt3=True)
    homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
    waiting_for_shower = False
  # Announce that the bathroom is ready to taking a shower
  if topic == "device/thermostat_bathroom" and waiting_for_shower:
    if payload["thermostatTemperatureAmbient"] >= payload["thermostatTemperatureSetpoint"]:
      alert.voice("disfruta de la ducha.", gpt3=True)
      waiting_for_shower = False

# Set a relax scene
def relax(homeware, alert, topic, payload):
  if topic == "device/scene_relajacion/deactivate":
    global scene_pre_state
    if not payload:
      # Activate scenes
      alert.voice("configuro un ambiente de relajación.", speaker="livingroom,bedroom", gpt3=True)
      # Save current status
      devices_id = ["light001", "light002", "light003", "light004", "hue_1", "rgb001", "rgb002", "rgb003"]
      for device_id in devices_id:
        scene_pre_state[device_id] = homeware.get(device_id, "all")
      # Turn on some lights
      turn_on_devices = ["light003", "rgb001", "rgb002", "rgb003"]
      for control_id in turn_on_devices:
        homeware.execute(control_id, "on", True)
      # Turn off some lights
      turn_off_devices = ["light001", "light002", "light004", "hue_1"]
      for control_id in turn_off_devices:
        homeware.execute(control_id, "on", False)
    else:
      # Deactivate scene
      devices_id = ["light001", "light002", "light003", "light004", "hue_1", "rgb001", "rgb002", "rgb003"]
      for device_id in devices_id:
        device_state = scene_pre_state[device_id]
        for param in device_state:
          homeware.execute(device_id, param, device_state[param])

# Set the power alert scene
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
            # Send voice and text alerts
            alert.voice("Sobrecarga de potencia, nivel crítico")
            alert.message("Sobrecarga de potencia")
            # Change the status of some lights
            currentToggleSettings = {
              "emergencia": True
            }
            devices_id = ["rgb001", "rgb002", "rgb003"]
            for device_id in devices_id:
              homeware.execute(device_id, "currentToggleSettings", currentToggleSettings)
        if power < 85:
          if power_alert_counter > 1:
            power_alert_counter = 0
            # Send voice alerts
            alert.voice("Sistemas de potencia bajo control")
            currentToggleSettings = {
              "emergencia": False
            }
            devices_id = ["rgb001", "rgb002", "rgb003"]
            for device_id in devices_id:
              homeware.execute(device_id, "currentToggleSettings", currentToggleSettings)
          
          if power_alert_counter == 1:
            power_alert_counter = 0

# Set night scene
def night(homeware, topic, payload):
  # Day
  if topic == "device/scene_noche/deactivate" and payload:
    # Change some devices color
    color = {
      "spectrumRGB": 16741656,
      "spectrumRgb": 16741656
    }
    devices_ids = ["rgb001", "rgb002", "rgb003"]
    for device_id in devices_ids:
      homeware.execute(device_id, "color", color)
    # Change color temp on lights
    devices_ids = ["hue_2","hue_3"]
    for device_id in devices_ids:
      homeware.execute(device_id, "color", {"temperature": 6000})
    # Attenuate some lights
    devices_ids = ["hue_2","hue_3"]
    for device_id in devices_ids:
      homeware.execute(device_id, "brightness", 80)
  # Night
  elif topic == "device/scene_noche/deactivate" and not payload:
    # Change some devices color
    color = {
      "spectrumRGB": 16729344,
      "spectrumRgb": 16729344
    }
    devices_ids = ["rgb001", "rgb002", "rgb003"]
    for device_id in devices_ids:
      homeware.execute(device_id, "color", color)
    # Change a thermostat
    homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 20)
    # Change color temp on lights
    devices_ids = ["hue_2","hue_3"]
    for device_id in devices_ids:
      homeware.execute(device_id, "color", {"temperature": 2700})
    # Attenuate some lights
    devices_ids = ["hue_2","hue_3"]
    for device_id in devices_ids:
      homeware.execute(device_id, "brightness", 40)
