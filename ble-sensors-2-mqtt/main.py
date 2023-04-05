from bluepy import btle
import paho.mqtt.client as mqtt
import google.cloud.logging as logging
import os
import time

from homeware import Homeware

if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST_NETWORK", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
SERVICE = "ble-sensors-2-mqtt-" + ENV
# MAC address
DEVICES = {
  "thermostat_livingroom": {
    "mac": "F1:1C:1C:76:7F:3C",
  }
}
# API UUIDs
API_SERVICE_UUID ="cba20d00-224d-11e6-9fb8-0002a5d5c51b"
API_TX_CHARACTERISTIC_UUID= "cba20003-224d-11e6-9fb8-0002a5d5c51b"
API_RX_CHARACTERISTIC_UUID= "cba20002-224d-11e6-9fb8-0002a5d5c51b"

# Declare vars
cHandles = {}
ble_link = {}
rx_char = {}

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = logging.Client().logger(SERVICE)
homeware = Homeware(mqtt_client)

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, logger):
        self.logger = logger
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        if cHandle in cHandles:
          device_id = cHandles[cHandle]
          if data[0] == 1:
              if len(data) == 5:
                  # Update batery
                  homeware.execute(device_id,"capacityRemaining",[{"rawValue": data[1], "unit":"PERCENTAGE"}])
              elif len(data) == 4:
                  # Update temperature and humidity
                  temp_int = (data[2] - 128) if data[2] >= 128 else (data[2] * -1)
                  temp_dec = data[1] if data[1] < 16 else 0
                  temp = temp_int + (temp_dec/10)
                  hum = data[3] if data[3] < 128 else (data[3] - 128)           
                  homeware.execute(device_id,"thermostatTemperatureAmbient",temp)
                  homeware.execute(device_id,"thermostatHumidityAmbient",hum)
                  homeware.execute(device_id,"online",True)
              else:
                  self.logger.log_text("Unknown package from " + device, severity="WARNING")
          elif data[0] == 7:
              self.logger.log_text("Low battery: " + device, severity="WARNING")
              homeware.execute(device_id,"online",False)
        else:
            self.logger.log_text("Unknown handle", severity="WARNING")
# Main entry point
if __name__ == "__main__":
  logger.log_text("Starting", severity="INFO")
  # Check env vars
  def report(message):
    print(message)
    logger.log_text(message, severity="ERROR")
    exit()
  if MQTT_USER == "no_set":
    report("MQTT_USER env vars no set")
  if MQTT_PASS == "no_set":
    report("MQTT_PASS env vars no set")
  if MQTT_HOST == "no_set":
    report("MQTT_HOST env vars no set")
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

  while True:
    for device in DEVICES:
      try:
        if not device in ble_link:
          # Connect to device
          logger.log_text("Connecting to: " + device, severity="INFO")
          print("Connecting to:", device)
          ble_link[device] = btle.Peripheral(DEVICES[device]["mac"], btle.ADDR_TYPE_RANDOM, )
          ble_link[device].withDelegate( MyDelegate(logger) )
          # Get the API service
          service_uuid = btle.UUID(API_SERVICE_UUID)
          ble_service = ble_link[device].getServiceByUUID(service_uuid)
          # Set the notifications
          tx_uuid = btle.UUID(API_TX_CHARACTERISTIC_UUID)
          tx_char = ble_service.getCharacteristics(tx_uuid)[0]
          setup_data = b"\x01\x00"
          cHandle = tx_char.valHandle
          ble_link[device].writeCharacteristic(cHandle + 1, setup_data)
          cHandles[cHandle] = device
          # Get API RX the characteristic
          rx_uuid = btle.UUID(API_RX_CHARACTERISTIC_UUID)
          rx_char[device] = ble_service.getCharacteristics(rx_uuid)[0]
          time.sleep(5)
        if device in ble_link:
          # Request temperature and humidity
          rx_char[device].write(bytes.fromhex("570f31"))
          ble_link[device].waitForNotifications(5)
          # Request device info
          rx_char[device].write(bytes.fromhex("570200"))
          ble_link[device].waitForNotifications(5)
      except btle.BTLEDisconnectError:
        logger.log_text("Device offline: " + device, severity="WARNING")
        homeware.execute(device,"online",False)
        if device in ble_link:
          del ble_link[device]
    time.sleep(30)