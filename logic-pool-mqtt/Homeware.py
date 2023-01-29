import json
import requests

class Homeware:

  __mqtt_client = None
  __host = "localhost"
  __token = "token"

  def __init__(self, mqtt_client, host, token):
    self.__mqtt_client = mqtt_client
    self.__host = host
    self.__token = token

  def execute(self, id, param, value):    
    control_payload = {
      "id": id,
      "param": param,
      "value": value,
      "intent": "execute"
    }
    self.__mqtt_client.publish("device/control", json.dumps(control_payload))

  def get(self, id, param):
    url = "http://" + self.__host + "/api/status/get/" + id
    headers = {"Authorization": "baerer " + self.__token}
    response = requests.get(url, headers=headers)
    return response.json()[param]
  
  def voiceAlert(self, text):
    self.__mqtt_client.publish("voice-alerts", text)

  def messageAlert(self, text):
    self.__mqtt_client.publish("message-alerts", text)