from bluepy import btle

# MAC address.
BLE_ADDRESS = "F1:1C:1C:76:7F:3C"
# API UUIDs
API_SERVICE_UUID ="cba20d00-224d-11e6-9fb8-0002a5d5c51b"
API_TX_CHARACTERISTIC_UUID= "cba20003-224d-11e6-9fb8-0002a5d5c51b"
API_RX_CHARACTERISTIC_UUID= "cba20002-224d-11e6-9fb8-0002a5d5c51b"


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
            exit()
        elif data[0] == 7:
            print("low batery")
            exit()
    

print("Connecting...")
dev = btle.Peripheral(BLE_ADDRESS, btle.ADDR_TYPE_RANDOM)
dev.withDelegate( MyDelegate() )
# Get the API service
service_uuid = btle.UUID(API_SERVICE_UUID)
ble_service = dev.getServiceByUUID(service_uuid)
# Set the notifications
tx_uuid = btle.UUID(API_TX_CHARACTERISTIC_UUID)
tx_char = ble_service.getCharacteristics(tx_uuid)[0]
setup_data = b"\x01\x00"
dev.writeCharacteristic(tx_char.valHandle + 1, setup_data)
# Request temperature and humidity
rx_uuid = btle.UUID(API_RX_CHARACTERISTIC_UUID)
rx_char = ble_service.getCharacteristics(rx_uuid)[0]
rx_char.write(bytes.fromhex("570f31"))

while True:
    if dev.waitForNotifications(1.0):
        continue
    print("Waiting...")