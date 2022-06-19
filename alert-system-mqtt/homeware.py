import requests
import json
import os

class Homeware:

  __api_key = ""
  __domain = ""

  def __init__(self):
    if os.environ.get("HOMEWARE_DOMAIN", "localhost") == "localhost":
      from dotenv import load_dotenv
      load_dotenv(dotenv_path="../.env")

    self.__api_key = os.environ.get("HOMEWARE_API_KEY", "no_api_key")
    self.__domain = os.environ.get("HOMEWARE_DOMAIN", "localhost")

  def getHomewareTest(self):
    response = requests.get("https://" + self.__domain + "/test").text
    return response

  def getDevices(self):
    url = "https://" + self.__domain + "/api/status/get/"
    headers = {
        "Authorization": "baerer " + self.__api_key
    }

    response = requests.get(url, headers=headers)
    devicesUnordered = response.json()

    return devicesUnordered

  def setParam(self, id, param, value):
    url = "https://" + self.__domain + "/api/status/update/"
    headers = {
        "Authorization": "baerer " + self.__api_key,
        "Content-Type": "application/json"
    }
    body = {
        "id": id,
        "param": param,
        "value": value
    }

    response = requests.post(url, data=json.dumps(body), headers=headers)

    return response.text