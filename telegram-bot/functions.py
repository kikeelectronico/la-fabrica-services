import os
import requests

if os.environ.get("HOMEWARE_APIKEY", "no_api_key") == "no_api_key":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

HOMEWARE_APIKEY = os.environ.get("HOMEWARE_APIKEY", "no_api_key")
HOMEWARE_API_HOST = os.environ.get("HOMEWARE_API_HOST", "no_domain")
GET_IP_ENDPOINT = os.environ.get("GET_IP_ENDPOINT", "no_ip")

def getPublicIP():
    ip = requests.get(GET_IP_ENDPOINT).text
    return ip

def getHomewareTest():
    response = requests.get("https://" + HOMEWARE_API_HOST + "/test").text
    return response