
HUMIDITY_TRIGGER = 60

def humidity(homeware, topic, payload):
  if topic == "device/thermostat_bathroom":
    homeware.execute("hood001", "on", payload["thermostatHumidityAmbient"] > HUMIDITY_TRIGGER)
      
