import os
import requests

if os.environ.get("HOMEWARE_APIKEY", "no_api_key") == "no_api_key":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

HOMEWARE_APIKEY = os.environ.get("HOMEWARE_APIKEY", "no_api_key")
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "no_domain")

def getPublicIP():
    ip = requests.get('http://rinconingenieril.es/ip.php').text
    return ip

def getHomewareTest():
    response = requests.get("https://" + HOMEWARE_DOMAIN + "/test").text
    return response