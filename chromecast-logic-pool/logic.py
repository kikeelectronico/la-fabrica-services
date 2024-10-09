import time

prev_player_playing_state = False 

def playingLights(homeware):
  global prev_player_playing_state
  if not prev_player_playing_state:
    homeware.execute("hue_4", "on", False)
    homeware.execute("hue_5", "on", False)
    time.sleep(0.5)
    homeware.execute("hue_1", "on", False)
    time.sleep(0.5)
    homeware.execute("hue_9", "on", False)
    homeware.execute("hue_10", "on", False)
    if homeware.get("thermostat_livingroom", "thermostatMode") == "cool":
      homeware.execute("thermostat_livingroom", "thermostatMode", "off")
    prev_player_playing_state = True
      
def notPlayingLights(homeware):
  global prev_player_playing_state
  if prev_player_playing_state:
    # if homeware.get("c8bd20a2-69a5-4946-b6d6-3423b560ffa9", "brightness") < 25:
    #   homeware.execute("hue_1", "on", True)
    #   homeware.execute("hue_9", "on", True)
    #   homeware.execute("hue_10", "on", True)
    prev_player_playing_state = False
