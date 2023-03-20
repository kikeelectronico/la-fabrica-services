import os
import requests
from io import BytesIO
import time
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from google.cloud import bigquery

class Spotify:

  __refresh_token = ""
  __app_auth = ""
  __access_token = ""
  _tries = 0
  _playing = {}
  _last_track = ""
  _track_image = ""
  _track_image_position = "middle"
  _stop_until = 0
  _service_unavailable_counter = 0

  def __init__(self):
    if os.environ.get("SPOTIFY_REFRESH_TOKEN", "no") == "no":
      from dotenv import load_dotenv
      load_dotenv(dotenv_path="../.env")
    self.__refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
    self.__app_auth = os.environ.get("SPOTIFY_APP_AUTH")
    self._covers_ddbb = os.environ.get("COVERS_DDBB", "no_ddbb")
    # Initialize the keras model
    np.set_printoptions(suppress=True)
    self._track_image_model = load_model("track_image_model/keras_model.h5", compile=False)
    self._track_image_class_names = open("track_image_model/labels.txt", "r").readlines()
    self._track_image_data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Connect with bigquery
    self._bigquery_client = bigquery.Client()

  def updatePlaying(self, max_tries=2, logger=None):
    self._tries += 1
    if self.__access_token == "":
      self.updateAccessToken(logger)
    try:
      # Plaiyng
      url = "https://api.spotify.com/v1/me/player/"
      payload={}
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self.__access_token
      }
      response = requests.request("GET", url, headers=headers, data=payload, timeout=5)

      if response.status_code == 200:
        self._service_unavailable_counter = 0
        playing = response.json()
        if playing['is_playing'] and not playing["item"] is None:
          if not self._last_track == playing['item']['id'] and time.time() > self._stop_until:
            # Track info
            url= "https://api.spotify.com/v1/tracks/" + playing['item']['id']
            payload={}
            headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + self.__access_token
            }
            response = requests.request("GET", url, headers=headers, data=payload, timeout=5)

            if response.status_code == 200:
              track = response.json()
              self._track_image = track['album']['images'][0]['url']
              self._last_track = playing['item']['id']

              self.analyzeTrackImage(logger)

              # Save the image url
              self._bigquery_client.query(
                  """
                    INSERT INTO `{}`
                    (url, downloaded)
                    VALUES ('{}',False);
                  """.format(self._covers_ddbb, self._track_image)
              )

              spotify = {
                "playing": playing['is_playing'],
                "device": playing['device']['name'],
                "volume": playing['device']['volume_percent'],
                "track_name": playing['item']['name'],
                "time": playing['progress_ms'],
                "duration": playing['item']['duration_ms'],
                "artists": ", ".join([artist["name"] for artist in playing['item']['artists']]),
                "image": self._track_image,
                "image_position": self._track_image_position,
                "tries": self._tries,
                "quota_exceeded": False
              }

              self._tries = 0
              self._playing = spotify

            elif response.status_code == 429:
              logger.log_text("Spotify API quota exceeded", severity="WARNING")
              self._stop_until = time.time() + (int(response.headers['retry-after'])*1000)

              spotify = {
                "playing": playing['is_playing'],
                "device": playing['device']['name'],
                "volume": playing['device']['volume_percent'],
                "track_name": playing['item']['name'],
                "time": playing['progress_ms'],
                "duration": playing['item']['duration_ms'],
                "artists": ", ".join([artist["name"] for artist in playing['item']['artists']]),
                "image": "",
                "image_position": self._track_image_position,
                "tries": self._tries,
                "quota_exceeded": True
              }

              self._playing = spotify
          
          else:
            spotify = {
                "playing": playing['is_playing'],
                "device": playing['device']['name'],
                "volume": playing['device']['volume_percent'],
                "track_name": playing['item']['name'],
                "time": playing['progress_ms'],
                "duration": playing['item']['duration_ms'],
                "artists": ", ".join([artist["name"] for artist in playing['item']['artists']]),
                "image": self._track_image,
                "image_position": self._track_image_position,
                "tries": self._tries,
                "quota_exceeded": time.time() < self._stop_until
              }

            self._tries = 0
            self._playing = spotify

        else:
          spotify = {
            "playing": False,
            "tries": self._tries,
            "quota_exceeded": False
          }

          self._tries = 0
          self._playing = spotify

      elif response.status_code == 204:
        logger.log_text("Spotify API returns a 204 code", severity="INFO")
        spotify = {
          "playing": False,
          "tries": self._tries,
          "quota_exceeded": False
        }

        self._playing = spotify

      elif response.status_code == 429:
        logger.log_text("Spotify API quota exceeded", severity="WARNING")
        spotify = {
          "playing": False,
          "tries": self._tries,
          "quota_exceeded": True
        }

        self._playing = spotify

      elif response.status_code == 503:
        logger.log_text("Spotify API returns a 503 code", severity="INFO")
        if self._service_unavailable_counter == 0:
          self._service_unavailable_counter += 1
        else:
          spotify = {
            "playing": False,
            "tries": self._tries,
            "quota_exceeded": False
          }

          self._playing = spotify

      else:
        error = response.json()['error']
        logger.log_text("Spotify API returns a " + error['status'] + " code", severity="INFO")
        spotify = {
          "playing": False,
          "tries": self._tries,
          "quota_exceeded": False
        }

        if error['status'] == 400 or error['status'] == 401:
          if self.updateAccessToken() and self._tries < max_tries:
            self._playing = self.getPlaying(max_tries)
          else:
            self._playing = spotify
        else:
          self._playing = spotify

    except (requests.ConnectionError, requests.Timeout) as exception:
      logger.log_text("Fail to get Spotify player data. Conection error.", severity="WARNING")
      spotify = {
        "playing": False,
        "tries": self._tries,
        "quota_exceeded": False
      }

  def updateAccessToken(self, logger):
    try:
      logger.log_text("Updating Spotify access token", severity="INFO")
      url = "https://accounts.spotify.com/api/token"
      payload='grant_type=refresh_token&refresh_token=' + self.__refresh_token
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Basic ' + self.__app_auth
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
      if response.status_code == 200:
        self.__access_token = response.json()['access_token']
        logger.log_text("Spotify access token updated", severity="INFO")
        return True
      else:
        logger.log_text("Fail to update Spotify access token. Status code: " + response.status_code, severity="WARNING")
        return False
    except (requests.ConnectionError, requests.Timeout) as exception:
      logger.log_text("Fail to update Spotify access token. Conection error.", severity="WARNING")
      return False

  def getPlaying(self, max_tries=2, logger=None):
    self.updatePlaying(max_tries, logger)

    return self._playing

  def analyzeTrackImage(self, logger):
    try:
      response = requests.get(self._track_image)
      image = Image.open(BytesIO(response.content)).convert("RGB")

      if response.status_code == 200:
        try:
          size = (224, 224)
          image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
          image_array = np.asarray(image)
          normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
          self._track_image_data[0] = normalized_image_array

          prediction = self._track_image_model.predict(self._track_image_data)
          index = np.argmax(prediction)
          class_name = self._track_image_class_names[index]
          self._track_image_position = class_name[2:-1]
        except:
          logger.log_text("Fail to analyze a track image from Spotify", severity="WARNING")
      else:
        logger.log_text("Fail to get a track image from Spotify. Error code: " + response.status_code, severity="WARNING")
    except (requests.ConnectionError, requests.Timeout) as exception:
      logger.log_text("Fail to get a track image from Spotify. Conection error.", severity="WARNING")