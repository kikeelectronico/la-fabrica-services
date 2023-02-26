import requests
import json
from requests.exceptions import ConnectionError

# Test both the API and the db getting the status of a device
def homewareTest(api_url, api_key):
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
  
# Test Hue Bridge
def hueTest(api_url, api_token):     
  try:
    url = "http://" + api_url + "/api/" +	api_token + "/lights"
    response = requests.get(url)
                
    if response.status_code == 200:
      return True
    else:
      return False
  except ConnectionError:
    return False