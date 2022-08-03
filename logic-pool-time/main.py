import time
import datetime
import homeware

if __name__ == "__main__":
  while True:
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")

    if hour == "08:00:00":
      homeware.setParam("hood001", "on", True)
    elif hour == "12:00:00":
      homeware.setParam("hood001", "on", False)
    elif hour == "22:00:00":
      homeware.setParam("hood001", "on", True)
    elif hour == "06:00:00":
      homeware.setParam("hood001", "on", False)
