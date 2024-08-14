prev_player_playing_state = False 

def playingLights(homeware):
  homeware.execute("hue_1", "on", False)
  homeware.execute("hue_9", "on", False)
  homeware.execute("hue_10", "on", False)
  homeware.execute("hue_4", "on", False)
  homeware.execute("hue_5", "on", False)
  homeware.execute("light004", "on", False)
  global prev_player_playing_state
  prev_player_playing_state = True
      
def notPlayingLights(homeware):
  global prev_player_playing_state
  if prev_player_playing_state:
    if homeware.get("c8bd20a2-69a5-4946-b6d6-3423b560ffa9", "brightness") < 25:
      homeware.execute("hue_1", "on", True)
      homeware.execute("hue_9", "on", True)
      homeware.execute("hue_10", "on", True)
    prev_player_playing_state = False
