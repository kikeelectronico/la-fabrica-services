from bluepy import btle
import os
import paho.mqtt.client as mqtt

from homeware import Homeware

if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")

# Define constants
MQTT_PORT = 1883
# MAC address
DEVICES = {
  "livingroom": {
    "mac": "F1:1C:1C:76:7F:3C",
    "homeware_id": "thermostat_livingroom"
  }
}
# API UUIDs
API_SERVICE_UUID ="cba20d00-224d-11e6-9fb8-0002a5d5c51b"
API_TX_CHARACTERISTIC_UUID= "cba20003-224d-11e6-9fb8-0002a5d5c51b"
API_RX_CHARACTERISTIC_UUID= "cba20002-224d-11e6-9fb8-0002a5d5c51b"

# Declare vars
cHandles = {}

# Instantiate objects
mqtt_client = mqtt.Client(client_id="ble-sensors-2-mqtt")
homeware = Homeware(mqtt_client, )

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        if data[0] == 1:
            temp_int = (data[2] - 128) if data[2] >= 128 else (data[2] * -1)
            temp_dec = data[1] if data[1] < 16 else 0
            temp = temp_int + (temp_dec/10)
            hum = data[3] if data[3] < 128 else (data[3] - 128)
            print(temp, hum)
            if cHandle in cHandles:
              device_id = cHandles[cHandle]
              homeware.execute(DEVICES[device_id]["homeware_id"],"thermostatTemperatureAmbient",temp)
            else:
               print("Unknown handle")
        elif data[0] == 7:
            print("low batery")

# Main entry point
if __name__ == "__main__":
  # Check env vars
  if MQTT_USER == "no_set":
    print("MQTT_USER env vars no set")
    exit()
  if MQTT_PASS == "no_set":
    print("MQTT_PASS env vars no set")
    exit()
  if MQTT_HOST == "no_set":
    print("MQTT_HOST env vars no set")
    exit()
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  #mqtt_client.publish("message-alerts", "Hue 2 MQTT: operativo")

  print("Connecting...")
  dev = {}
  tx_char = {}
  rx_char = {}
  for device in DEVICES:
    # Connect to device
    dev[device] = btle.Peripheral(DEVICES[device]["mac"], btle.ADDR_TYPE_RANDOM)
    dev[device].withDelegate( MyDelegate() )
    # Get the API service
    service_uuid = btle.UUID(API_SERVICE_UUID)
    ble_service = dev[device].getServiceByUUID(service_uuid)
    # Set the notifications
    tx_uuid = btle.UUID(API_TX_CHARACTERISTIC_UUID)
    tx_char[device] = ble_service.getCharacteristics(tx_uuid)[0]
    setup_data = b"\x01\x00"
    cHandle = tx_char[device].valHandle
    dev[device].writeCharacteristic(cHandle + 1, setup_data)
    cHandles[cHandle] = device
    # Get API RX the characteristic
    rx_uuid = btle.UUID(API_RX_CHARACTERISTIC_UUID)
    rx_char[device] = ble_service.getCharacteristics(rx_uuid)[0]

  while True:
    for device in DEVICES:
      if dev[device].waitForNotifications(5):
          continue
      # Request temperature and humidity
      rx_char[device].write(bytes.fromhex("570f31"))
    print("Waiting...")