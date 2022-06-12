import time
from pychromecast import Chromecast
from pychromecast.controllers.dashcast import DashCastController


CHROMECAST_IP = "192.168.10.204"
TRIGGER_APP = "Backdrop"
WEB_PANEL = "http://192.168.10.2:81"
TEST = False

# Connect to the Chromcast
cast = Chromecast(CHROMECAST_IP, tries=None, timeout=3, retry_wait=5)
cast.wait()

dash = DashCastController()
cast.register_handler(dash)

while True:
  # It is the trigger app?
  if cast.status.display_name == TRIGGER_APP:
    if TEST:
      dash.load_url(url="https://www.google.com", force=True)
    else:
      dash.load_url(url=WEB_PANEL, force=True)
  
  time.sleep(5)