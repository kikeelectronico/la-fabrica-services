import requests

class Hue:
  
  __url = "localhost"
  __token = "token"

  def __init__(self, url, token):
    self.__url = url
    self.__token = token
    
  # Get lights json
  def getLights(self):
    url = "http://" + self.__url + "/api/" +	self.__token + "/lights"
    response = requests.get(url)
    return response.json()
  
  # Get lights json
  def getSensors(self):
    url = "http://" + self.__url + "/api/" +	self.__token + "/sensors"
    response = requests.get(url)
    return response.json()