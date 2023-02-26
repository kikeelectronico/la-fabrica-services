import requests
from requests.exceptions import ConnectionError

# Test both the API and the db getting the status of a device
def getHomewareTest(api_url, api_key):
  try:
    url = api_url + "/api/status/get/scene_noche"
    headers = {
        "Authorization": "baerer " + api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      status = response.json()
      return "deactivate" in status
    else:
      return False
  except ConnectionError:
    return False