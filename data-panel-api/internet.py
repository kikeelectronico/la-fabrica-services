import requests

class Internet:

  _connected = True

  def __init__(self, logger):
    self.logger = logger

  def checkConnectivity(self):
    try:
      requests.get("https://www.google.com", timeout=2)
      self._connected = True
    except (requests.ConnectionError, requests.Timeout) as exception:
      self.logger.log_text("Fail to reach Google. Conection error.", severity="WARNING")
      self._connected = False
      
    try:
      requests.get("https://www.cloudflare.com/", timeout=2)
      self._connected = True
    except (requests.ConnectionError, requests.Timeout) as exception:
      self.logger.log_text("Fail to reach Cloudflare. Conection error.", severity="WARNING")
      self._connected = self._connected and False
    
    return self._connected

  def getConnected(self):
    return self._connected