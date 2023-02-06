import os
import requests
import json
import time

class Spotify:

  __refresh_token = ""
  __app_auth = ""
  __access_token = ""
  _tries = 0
  _playing = {}
  _last_track = ""
  _track_image = ""
  _stop_until = 0
  _service_unavailable_counter = 0

  def __init__(self):
    if os.environ.get("SPOTIFY_REFRESH_TOKEN", "no") == "no":
      from dotenv import load_dotenv
      load_dotenv(dotenv_path="../.env")
    self.__refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
    self.__app_auth = os.environ.get("SPOTIFY_APP_AUTH")
    # Temp for analysis
    self.__injector_url = os.environ.get("INJECTOR_URL", "no_url")
    self.__injector_token = os.environ.get("INJECTOR_TOKEN", "no_token")


  def updatePlaying(self, max_tries=2):
    self._tries += 1
    if self.__access_token == "":
      self.updateAccessToken()
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
        if playing['is_playing']:
          if "item" in playing.keys() and "id" in playing['item'].keys():
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

                spotify = {
                  "playing": playing['is_playing'],
                  "device": playing['device']['name'],
                  "volume": playing['device']['volume_percent'],
                  "track_name": playing['item']['name'],
                  "time": playing['progress_ms'],
                  "duration": playing['item']['duration_ms'],
                  "artists": ", ".join([artist["name"] for artist in playing['item']['artists']]),
                  "image": self._track_image,
                  "tries": self._tries,
                  "quota_exceeded": False
                }

                self._tries = 0
                self._playing = spotify

                # Temp for analisys
                url = self.__injector_url + "?token=" + self.__injector_token
                headers = {
                  "Content-Type": "application/json"
                }
                body = {
                  "ddbb": "covers",
                  "URL": self._track_image
                }

                requests.post(url, data = json.dumps(body), headers = headers)

              elif response.status_code == 429:
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
        spotify = {
          "playing": False,
          "tries": self._tries,
          "quota_exceeded": False
        }

        self._playing = spotify

      elif response.status_code == 429:
        spotify = {
          "playing": False,
          "tries": self._tries,
          "quota_exceeded": True
        }

        self._playing = spotify

      elif response.status_code == 503:
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
      spotify = {
        "playing": False,
        "tries": self._tries,
        "quota_exceeded": False
      }

  def updateAccessToken(self):
    try:
      url = "https://accounts.spotify.com/api/token"
      payload='grant_type=refresh_token&refresh_token=' + self.__refresh_token
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Basic ' + self.__app_auth
      }

      response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
      if response.status_code == 200:
        self.__access_token = response.json()['access_token']
        return True
      else:
        return False
    except (requests.ConnectionError, requests.Timeout) as exception:
      return False

  def getPlaying(self, max_tries=2):
    self.updatePlaying(max_tries)

    return self._playing