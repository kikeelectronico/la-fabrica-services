import os
import requests
import json

class Homeware:

  __api_key = ""
  __domain = ""

  def __init__(self):
    if os.environ.get("HOMEWARE_API_KEY", "no") == "no":
      from dotenv import load_dotenv
      load_dotenv(dotenv_path="../.env")
    self.__api_key = os.environ.get("HOMEWARE_API_KEY")
    self.__url = os.environ.get("HOMEWARE_API_URL")

  def getStatus(self):
    url = self.__url + "/api/status/get/"
    headers = {
        "Authorization": "baerer " + self.__api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      status = response.json()
      return (True, status)
    else:
      return (False, {})

  def getDevices(self):
    url = self.__url + "/api/devices/get/"
    headers = {
        "Authorization": "baerer " + self.__api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      unorderedDevices = response.json()
      devices = {}
      for device in unorderedDevices:
          devices[device['id']] = device
      return (True, devices)
    else:
      return (False, {})


    

