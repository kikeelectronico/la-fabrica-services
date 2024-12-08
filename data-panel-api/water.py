import time
from selenium import webdriver

RELOAD_TIME = 3600

class Water:

  _level = -1
  _last_update = "No date"
  _last_request = 0

  def __init__(self, logger):
    self.logger = logger

  def updateWater(self):
    try:
      options = webdriver.ChromeOptions()
      options.add_argument("--headless=chrome")
      options.add_argument("--disable-gpu")
      options.add_argument("--disable-dev-shm-usage")
      options.add_argument("--no-sandbox")

      driver = webdriver.Chrome(options=options)
      driver.get("https://www.embalses.net/comunidad-13-comunidad-de-madrid.html")

      self._last_update = driver.find_element("xpath", '//*[@id="index_bodycenter"]/div[2]/div[2]/div[3]/div[1]/strong').get_attribute("innerHTML")
      self._last_update = self._last_update.split("(")[1].split(")")[0]
      self._level = driver.find_element("xpath", '//*[@id="index_bodycenter"]/div[2]/div[2]/div[3]/div[4]/strong').get_attribute("innerHTML")
      self._level = float(self._level)
      driver.quit()
    except:
      self.logger.log("Fail to reach embalses.net.", severity="WARNING")

  def getWater(self):
    now = time.time()
    if now - self._last_request > RELOAD_TIME:
      self._last_request = now
      self.updateWater()
    return {
      "level": self._level,
      "last_update": self._last_update
    }