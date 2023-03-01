import json

long_pressing = False

def entry(id, state, homeware):
    #print(id, state)
    mirrorLights(id, state, homeware)

def mirrorLights(id, state, homeware):
    global long_pressing
    if id == "2":
      if state["buttonevent"] == 1001:
          if not long_pressing:
            value = not homeware.get("switch_hood","on")
            homeware.execute("switch_hood","on",value)
            long_pressing = True

      elif state["buttonevent"] == 1003:
          long_pressing = False

      elif state["buttonevent"] == 1002:
          value = not homeware.get("hue_2","on")
          homeware.execute("hue_2","on",value)
          homeware.execute("hue_3","on",value)
      
      elif state["buttonevent"] == 2002:
          value = homeware.get("hue_2","brightness")
          if value < 90:
            value += 10
          else:
            value = 100
          homeware.execute("hue_2","brightness",value)
          homeware.execute("hue_3","brightness",value)
        
      elif state["buttonevent"] == 3002:
          value = homeware.get("hue_2","brightness")
          if value > 10:
            value -= 10
          else:
            value = 0
          homeware.execute("hue_2","brightness",value)
          homeware.execute("hue_3","brightness",value)

      elif state["buttonevent"] == 4002:
          current_temperature = homeware.get("hue_2","color")["temperature"]
          TEMPERATURE_LOOP = [2700, 6000]
          try:
              new_index = TEMPERATURE_LOOP.index(current_temperature) + 1
              if new_index == len(TEMPERATURE_LOOP): new_index = 0 
          except ValueError:
              new_index = 0
          new_temperature = TEMPERATURE_LOOP[new_index]
          homeware.execute("hue_2","color",{"temperature": new_temperature})
          homeware.execute("hue_3","color",{"temperature": new_temperature})