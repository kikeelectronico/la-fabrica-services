dimmers_preloaded_data = {}

def mirror(service, homeware):
    global dimmers_preloaded_data
    # On/off button
    if service["id"] == "eef00948-5ed7-4ec4-94dd-60da620887a1":
      state = service["button"]["last_event"]
      if state == "initial_press":
        dimmers_preloaded_data["hue_sensor_2/on"] = not homeware.get("hue_sensor_2","on")
      elif state == "short_release":
        homeware.execute("hue_sensor_2","on",dimmers_preloaded_data["hue_sensor_2/on"])
      elif state == "long_press":
        value = not homeware.get("switch_hood","on")
        homeware.execute("switch_hood","on",value)

    # More brightness button
    elif service["id"] == "13362cd4-0324-4dfb-97ec-c567c2cefb70":
      state = service["button"]["last_event"]
      if state == "initial_press":
        dimmers_preloaded_data["hue_2/brightness"] = homeware.get("hue_2","brightness")
      elif state == "short_release":
        value = dimmers_preloaded_data["hue_2/brightness"]
        if value < 90:
          value += 10
        else:
          value = 100
        homeware.execute("hue_2","brightness",value)
        homeware.execute("hue_3","brightness",value)
      elif state == "long_press":
        value = not homeware.get("scene_dim","enable")
        homeware.execute("scene_dim","enable",value)

    # Less brightness button
    elif service["id"] == "17bd6fda-f053-403e-ab85-4ab3efa77abe":
      state = service["button"]["last_event"]
      if state == "initial_press":
        dimmers_preloaded_data["hue_2/brightness"] = homeware.get("hue_2","brightness")
      elif state == "short_release":
        value = dimmers_preloaded_data["hue_2/brightness"]
        if value > 10:
          value -= 10
        else:
          value = 0
        homeware.execute("hue_2","brightness",value)
        homeware.execute("hue_3","brightness",value)
 
    # Hue button
    elif service["id"] == "ee82e035-fd34-45d8-bbf2-282980004c63":
      state = service["button"]["last_event"]
      if state == "initial_press":
        dimmers_preloaded_data["hue_2/color"] = homeware.get("hue_2","color")["temperatureK"]
      elif state == "short_release":
        current_temperature = dimmers_preloaded_data["hue_2/color"]
        TEMPERATURE_LOOP = [2700, 5000]
        try:
            new_index = TEMPERATURE_LOOP.index(current_temperature) + 1
            if new_index == len(TEMPERATURE_LOOP): new_index = 0 
        except ValueError:
            new_index = 0
        new_temperature = TEMPERATURE_LOOP[new_index]
        homeware.execute("hue_2","color",{"temperatureK": new_temperature})
        homeware.execute("hue_3","color",{"temperatureK": new_temperature})
