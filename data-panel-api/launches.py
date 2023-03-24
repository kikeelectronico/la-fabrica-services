import os
import requests
import json
import time
from datetime import datetime, timedelta

RELOAD_TIME = 3600

class Launches:

  _launches = {}
  _last_update = 0
  _fail_to_update = True

  def __init__(self, logger):
    # Set the logger
    self.logger = logger

  def updateLaunches(self):
    try:
      url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
      response = requests.request("GET", url, verify=False, timeout=5)
      if response.status_code == 200:
        launches = response.json()['results']
        self._launches = []
        for launch in launches:
          now = datetime.now()
          launch_date = datetime.strptime(launch['net'], '%Y-%m-%dT%H:%M:%SZ')
          if launch_date > now and launch_date < (now + timedelta(days=1)):
            self._launches.append(launch)

        self._fail_to_update = False
      else:
        self.logger.log_text("Fail to update launches. Status code: " + str(response.status_code), severity="WARNING")
        self._fail_to_update = True
    except (requests.ConnectionError, requests.Timeout) as exception:
      self.logger.log_text("Fail to update launches. Conection error.", severity="WARNING")
      self._fail_to_update = False

  def getLaunches(self):
    now = time.time()
    if now - self._last_update > RELOAD_TIME:
      self._last_update = now
      self.updateLaunches()

    launches_flag = len(self._launches) > 0

    return (self._fail_to_update, launches_flag, self._launches)