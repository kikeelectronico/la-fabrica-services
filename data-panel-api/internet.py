import requests

class Internet:

  _connected = True

  def checkConnectivity(self):
    try:
      request = requests.get("https://www.google.com", timeout=5)
      self._connected = True
      return True
    except (requests.ConnectionError, requests.Timeout) as exception:
      self._connected = False
      return False

  def getConnected(self):
    return self._connected