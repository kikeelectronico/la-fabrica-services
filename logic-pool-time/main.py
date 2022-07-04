import time
import datetime
import homeware

if __name__ == "__main__":
  while True:
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")

    if hour == "09:00:00":
      homeware.setParam("hood001", "on", True)
    elif hour == "11:00:00":
      homeware.setParam("hood001", "on", False)
