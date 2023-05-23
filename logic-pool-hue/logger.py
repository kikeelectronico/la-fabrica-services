import json

class Logger:
    
    __mqtt_client = None
    __service = "Unknown"

    def __init__(self, mqtt_client, service):
        self.__mqtt_client = mqtt_client
        self.__service = service

    def log(self, message, severity = "INFO"):
        if not self.__mqtt_client is None:
            payload = {
                "service": self.__service,
                "severity": severity,
                "message": message
            }
            self.__mqtt_client.publish("log", json.dumps(payload))
        else:
            print("No connection to mqtt broker")