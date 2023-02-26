import telebot
import os
from google.cloud import storage

import functions

# Load env vars
if os.environ.get("BOT_TOKEN", "no_token") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "no_set")
ENRIQUE_CHAT_ID = os.environ.get("ENRIQUE_CHAT_ID", "no_set")

# Declare variables
wait_flag = ""

# Instantiate objects
bot = telebot.TeleBot(BOT_TOKEN)
storage_client = storage.Client()

# Commands handler
@bot.message_handler(commands=['start', 'help','test','office','home','directions','yt'])
def send_welcome(message):
  if 'start' in message.text:
    bot.reply_to(message, "Hi, I am Leia Organa")
  elif 'help' in message.text:
    bot.reply_to(message, "I am sorry but I don't know you.")
  else:
    if str(message.from_user.id) == ENRIQUE_CHAT_ID:
        if 'test' in message.text:
            # Test an authenticated command
            response = functions.test()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'home' in message.text:
            # Test Homeware API and db
            response = functions.getHomewareTest()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'directions' in message.text:
            # Get the public IP
            response = functions.getPublicIP()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'yt' in message.text:
            # Download a YouTube video
            global wait_flag
            wait_flag = "yt"
            bot.send_message(ENRIQUE_CHAT_ID, "¿Qué URL quieres descargar?", parse_mode= 'Markdown')
    else:
        bot.reply_to(message, "I am sorry but I don't know you.")

# Global handler
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if str(message.from_user.id) == ENRIQUE_CHAT_ID:
        # Download the YouTube video once the URL is given
        if wait_flag == "yt":
            bot.send_message(ENRIQUE_CHAT_ID, "Descargando...", parse_mode= 'Markdown')
            url = message.text
            urls = functions.downloadYouTubeVideo(url, storage_client)
            bot.send_message(ENRIQUE_CHAT_ID, "Lo tenemos", parse_mode= 'Markdown')
            for url in urls:
                bot.send_message(ENRIQUE_CHAT_ID, url, parse_mode= 'Markdown')

# Main entry point
if __name__ == "__main__":
    # Check env vars
    if BOT_TOKEN == "no_set":
      print("BOT_TOKEN env vars no set")
      exit()
    if ENRIQUE_CHAT_ID == "no_set":
      print("ENRIQUE_CHAT_ID env vars no set")
      exit()
    # Main loop
    bot.infinity_polling()