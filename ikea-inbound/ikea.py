import requests

class Ikea:
  
  __url = "localhost"
  __token = "token"

  def __init__(self, host, token, logger):
    self.__host = host
    self.__token = token
    self.logger = logger
      
  # Get motion
  def getDevices(self, resource="all"):
    if self.__token == "no_set" or self.__url == "no_set":
      self._fail_to_update = True
      self.logger.log("Hue env vars aren't set", severity="ERROR")
    else:
      try:
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.__token}"
        })
        url = f"https://{self.__host}:8443/v1/devices"
        if resource != "all":
          url = f"{url}/{resource}"
        response = session.get(url, verify=False)
        response.raise_for_status()
        devices = response.json()
        return devices
      except (requests.ConnectionError, requests.Timeout) as exception:
          self.logger.log("Fail to get Ikea hub " + resource + ". Conection error.", severity="WARNING")
          self._fail_to_update = False
          if resource == "all": return []
          return {}