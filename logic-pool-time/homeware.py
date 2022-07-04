import requests
import json
import os

if os.environ.get("HOMEWARE_DOMAIN", "no_domain") == "no_domain":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

HOMEWARE_APIKEY = os.environ.get("HOMEWARE_API_KEY")
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN")

def setParam(id, param, value):
    url = "https://" + HOMEWARE_DOMAIN + "/api/status/update/"
    headers = {
        "Authorization": "baerer " + HOMEWARE_APIKEY,
        "Content-Type": "application/json"
    }
    body = {
        "id": id,
        "param": param,
        "value": value
    }

    response = requests.post(url, data=json.dumps(body), headers=headers)

    return response.text