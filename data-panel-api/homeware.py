import os
import requests

class Homeware:

  __api_key = ""
  __domain = ""

  def __init__(self, logger):
    if os.environ.get("HOMEWARE_API_KEY", "no") == "no":
      from dotenv import load_dotenv
      load_dotenv(dotenv_path="../.env")
    self.__api_key = os.environ.get("HOMEWARE_API_KEY", "no_set")
    if self.__api_key == "no_set": 
      logger.log("HOMEWARE_API_KEY no set", severity="ERROR")
    self.__url = os.environ.get("HOMEWARE_API_URL", "no_set")
    if self.__url == "no_set": 
      logger.log("HOMEWARE_API_URL no set", severity="ERROR")
    # Set the logger
    self.logger = logger

  def getStatus(self):
    if self.__api_key == "no_set" or self.__url == "no_set":
      self._fail_to_update = True
      self.logger.log("Homeware env vars aren't set", severity="ERROR")
    else:
      try:
        url = self.__url + "/api/status/get/"
        headers = {
            "Authorization": "bearer " + self.__api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
          status = response.json()
          return (True, status)
        else:
          self.logger.log("Fail to get Homeware status. Status code: " + str(response.status_code), severity="WARNING")
          return (False, {})
      except (requests.ConnectionError, requests.Timeout) as exception:
        self.logger.log("Fail to get Homeware status. Conection error.", severity="WARNING")
        self._fail_to_update = False


  def getDevices(self):
    if self.__api_key == "no_set" or self.__url == "no_set":
      self._fail_to_update = True
      self.logger.log("Homeware env vars aren't set", severity="ERROR")
    else:
      try:
        url = self.__url + "/api/devices/get/"
        headers = {
            "Authorization": "bearer " + self.__api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
          unorderedDevices = response.json()
          devices = {}
          for device in unorderedDevices:
              devices[device['id']] = device
          return (True, devices)
        else:
          self.logger.log("Fail to get Homeware devices. Status code: " + str(response.status_code), severity="WARNING")
          return (False, {})    
      except (requests.ConnectionError, requests.Timeout) as exception:
        self.logger.log("Fail to get Homeware devices. Conection error.", severity="WARNING")
        self._fail_to_update = False


    

