import time

DELAY_BETWEEN_POWER_ALERTS = 40

power_alert_counter = 0
last_power_check = 0
waiting_for_shower = False
initial_bathroom_humidity = 0

# Set dim scene
def dim(homeware, topic, payload):
  if topic == "device/scene_dim/enable":
    if payload:
      # Adjust bedroom lights
      if homeware.get("hue_6", "on"):
        homeware.execute("rgb003", "on", True)
        homeware.execute("hue_6", "on", False)
      # Adjust bathroom lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 3000})
        homeware.execute(device_id, "brightness", 20)
      if homeware.get("light001", "on"):
        homeware.execute("hue_sensor_2", "on", True)
        homeware.execute("light001", "on", False)
      # Adjust hall light
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 30) 
      # Adjust RGB strips
      devices_ids = ["rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16729344,
        "spectrumRgb": 16729344
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)
    else:
      # Adjust bedroom lights
      if homeware.get("rgb003", "on"):
        homeware.execute("hue_6", "on", True)
        homeware.execute("rgb003", "on", False)
      # Adjust bathroom lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 5000})
        homeware.execute(device_id, "brightness", 80)
      if homeware.get("hue_sensor_2", "on"):
        homeware.execute("light001", "on", True)
        homeware.execute("hue_sensor_2", "on", False)
      # Adjust hall light      
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 100)
      # Adjust RGB strips
      devices_ids = ["rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)

# Set the shower scene
def shower(homeware, alert, topic, payload):
  global waiting_for_shower
  if topic == "device/scene_ducha/enable":
    if payload:
      # Start preparing the bathroom
      # alert.voice("Crea una frase que informe al usuario de que vas a preparar el baño para que se duche.", speaker="livingroom,bedroom", gpt3=True)
      homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 25)
      homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
      waiting_for_shower = True
      global initial_bathroom_humidity
      initial_bathroom_humidity = homeware.get("thermostat_bathroom", "thermostatHumidityAmbient")
    else:
      # Return the bathroom to normal
      # alert.voice("Crea una frase que diga al usuario que esperas que haya disfrutado de la ducha.", speaker="bathroom", gpt3=True)
      homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
      waiting_for_shower = False
      if homeware.get("hue_sensor_14","on"):
        homeware.execute("hue_sensor_14","on",False)
  # Announce that the bathroom is ready to taking a shower
  if topic == "device/thermostat_bathroom" and waiting_for_shower:
    if payload["thermostatTemperatureAmbient"] >= payload["thermostatTemperatureSetpoint"]:
      alert.voice("El baño está listo", speaker="livingroom,bedroom", gpt3=False)
      waiting_for_shower = False

BATHROOM_HUMIDITY_DELTA = 10

def disableShowerScene(homeware, alert, topic, payload):
  if topic == "device/c8bd20a2-69a5-4946-b6d6-3423b560ffa9/occupancy":
    if payload == "OCCUPIED":
      if homeware.get("scene_ducha", "enable"):
        if homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4", "openPercent") == 0:
          global initial_bathroom_humidity
          if homeware.get("thermostat_bathroom", "thermostatHumidityAmbient") > initial_bathroom_humidity + BATHROOM_HUMIDITY_DELTA:
            homeware.execute("scene_ducha", "enable", False)
            alert.voice("He desactivado el modo ducha", speaker="livingroom", gpt3=False)

# Set the power alert scene
def powerAlert(homeware, alert, topic, payload):
  if topic == "device/control":
    if payload["id"] == "current001" and payload["param"] == "brightness":
      global last_power_check
      global power_alert_counter
      power = payload["value"]
      if time.time() - last_power_check > DELAY_BETWEEN_POWER_ALERTS:
        last_power_check = time.time()
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

