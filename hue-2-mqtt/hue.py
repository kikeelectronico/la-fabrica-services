import requests

class Hue:
  
  __url = "localhost"
  __token = "token"

  def __init__(self, url, token, logger):
    self.__url = url
    self.__token = token
    self.logger = logger
    
  # Get lights json
  def getLights(self):
    try:
      url = "http://" + self.__url + "/api/" +	self.__token + "/lights"
      response = requests.get(url)
      if response.status_code == 200:
        return response.json()
      else:
        self.logger.log_text("Fail to get Hue Bridge lights. Status code: " + str(response.status_code), severity="WARNING")
        return {}
    except (requests.ConnectionError, requests.Timeout) as exception:
        self.logger.log_text("Fail to get Hue Bridge lights. Conection error.", severity="WARNING")
        self._fail_to_update = False
        return {}