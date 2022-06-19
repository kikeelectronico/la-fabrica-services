import telebot
from Voice import Voice
import os
import time
import requests

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "no_token")
ENRIQUE_CHAT_ID = os.environ.get("ENRIQUE_CHAT_ID", "no_id")
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")
SLEEP_TIME = 10

bot = telebot.TeleBot(token=BOT_TOKEN)
voice = Voice()

public_IP_saved = 'unknow'

def getHomewareTest():
    response = requests.get("https://" + HOMEWARE_DOMAIN + "/test").text
    return response

def getPublicIP():
    ip = requests.get('http://rinconingenieril.es/ip.php').text
    return ip

def main():
    global public_IP_saved
    while True:
        try:
            ip = getPublicIP()
            if not ip == public_IP_saved:
                bot.send_message(ENRIQUE_CHAT_ID, 'Cambio de IP pública de Coruscant\r\n\r\n Actual: ' + str(ip) + '\r\nAbandonada: ' + str(public_IP_saved))
                voice.getAndPlay("Cambio de I P pública")
                public_IP_saved = ip

            if not getHomewareTest() == 'Load':
                bot.send_message(ENRIQUE_CHAT_ID, '*Homeware* caido', parse_mode= 'Markdown')
                voice.getAndPlay("Homeware se ha caido")

            time.sleep(SLEEP_TIME)
        except:
            time.sleep(10)

if __name__ == "__main__":
	main()

    