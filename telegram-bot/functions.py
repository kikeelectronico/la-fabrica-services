import os
import requests
from pytube import YouTube, Playlist

def getPublicIP(endpoint):
    ip = requests.get(endpoint).text
    return ip

def getHomewareTest(url, api_key):
    response = requests.get(url + "/test").text
    return response

def test():
  return "I think this is broken. It has a hole."

def downloadYouTubeVideo(url, storage_client, bucket):
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
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(file)
        blob.upload_from_filename(file)
        # Delete the local file
        os.remove(file)
        # Add URL
        urls.append("https://storage.cloud.google.com/" + bucket + "/" + file.replace(" ", "%20"))
    # Return URL
    return urls
