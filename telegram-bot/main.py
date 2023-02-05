import telebot
from pytube import YouTube, Playlist
import os
from google.cloud import storage

import functions

if os.environ.get("BOT_TOKEN", "no_token") == "no_token":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "no_token")
ENRIQUE_CHAT_ID = os.environ.get("ENRIQUE_CHAT_ID", "no_id")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "no_bucket")

wait_flag = ""

#Absolute path
ScriptPath = os.path.realpath(__file__).split('bot')[0]

bot = telebot.TeleBot(BOT_TOKEN)
storage_client = storage.Client()

def test():
  return "I think this is broken. It has a hole."

def downloadYouTubeVideo(url):
    if not 'list' in url:
        video = YouTube(url)
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    else:
        playlist = Playlist(url)
        for video in playlist.videos:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

    # Get the mp4 files
    all_in_dir = os.listdir('.')
    files = [something for something in all_in_dir if something.endswith('.mp4')]
    # Get the first file
    urls = []
    for file in files:
        # Upload to the bucket
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file)
        blob.upload_from_filename(file)
        # Delete the local file
        os.remove(file)
        # Add URL
        urls.append("https://storage.cloud.google.com/" + BUCKET_NAME + "/" + file.replace(" ", "%20"))
    # Return URL
    return urls

@bot.message_handler(commands=['start', 'help','test','office','home','directions','yt'])
def send_welcome(message):
  if 'start' in message.text:
    bot.reply_to(message, "Hi, I am Leia Organa")
  elif 'help' in message.text:
    bot.reply_to(message, "I am sorry but I don't know you.")
  else:
    if str(message.from_user.id) == ENRIQUE_CHAT_ID:
        if 'test' in message.text:
            response = test()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'home' in message.text:
            response = functions.getHomewareTest()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'directions' in message.text:
            response = functions.getPublicIP()
            bot.send_message(ENRIQUE_CHAT_ID, response, parse_mode= 'Markdown')
        elif 'yt' in message.text:
            global wait_flag
            wait_flag = "yt"
            bot.send_message(ENRIQUE_CHAT_ID, "¿Qué URL quieres descargar?", parse_mode= 'Markdown')
    else:
        bot.reply_to(message, "I am sorry but I don't know you.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.from_user.id == ENRIQUE_CHAT_ID:
        if wait_flag == "yt":
            bot.send_message(ENRIQUE_CHAT_ID, "Descargando...", parse_mode= 'Markdown')
            url = message.text
            urls = downloadYouTubeVideo(url)
            bot.send_message(ENRIQUE_CHAT_ID, "Lo tenemos", parse_mode= 'Markdown')
            for url in urls:
                bot.send_message(ENRIQUE_CHAT_ID, url, parse_mode= 'Markdown')

if __name__ == "__main__":
    bot.infinity_polling()