import os
import requests
from pytube import YouTube, Playlist

if os.environ.get("HOMEWARE_APIKEY", "no_api_key") == "no_api_key":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

HOMEWARE_APIKEY = os.environ.get("HOMEWARE_APIKEY", "no_api_key")
HOMEWARE_API_HOST = os.environ.get("HOMEWARE_API_HOST", "no_domain")
GET_IP_ENDPOINT = os.environ.get("GET_IP_ENDPOINT", "no_ip")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "no_bucket")

def getPublicIP():
    ip = requests.get(GET_IP_ENDPOINT).text
    return ip

def getHomewareTest():
    response = requests.get("https://" + HOMEWARE_API_HOST + "/test").text
    return response

def test():
  return "I think this is broken. It has a hole."

def downloadYouTubeVideo(url, storage_client):
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
