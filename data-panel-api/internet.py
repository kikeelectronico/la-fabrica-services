import requests

class Internet:

  _connected = True

  def __init__(self, logger):
    self.logger = logger

  def checkConnectivity(self):
    try:
      request = requests.get("https://www.google.com", timeout=5)
      self._connected = True
      return True
    except (requests.ConnectionError, requests.Timeout) as exception:
      self.logger.log_text("Fail to reach Google. Conection error.", severity="WARNING")
      self._connected = False
      return False

  def getConnected(self):
    return self._connected