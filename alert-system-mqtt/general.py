import json

store = {}
power_alert_counter = 0

def power(homeware, voice, topic, payload):
  if topic == "device/control":
    if payload["id"] == "switch003" and payload["param"] == "on":
        voice.getAndPlay("Alguien ha usado en interruptor de internet")
    if payload["id"] == "current001" and payload["param"] == "brightness":
        power = payload["value"]
        global store
        global power_alert_counter
        # Power alerts
        if power >= 90:
            # Get home devices status
            devices = homeware.getDevices()
            store["rgb001"] = {
                "color": devices["rgb001"]["color"],
                "on": devices["rgb001"]["on"]
            }
            color = {
                "spectrumRGB": 16711680,
                "spectrumRgb": 16711680
            }
            homeware.setParam("rgb001", "color", color)
            homeware.setParam("rgb001", "on", True)

        if power >= 100:
            power_alert_counter += 1
            voice.getAndPlay("Sobrecarga de potencia, nivel crítico")
        elif power_alert_counter <= 3 and power >= 90:
            power_alert_counter += 1
            voice.getAndPlay("Sobrecarga de potencia, nivel 9")
        
        if power_alert_counter >= 1 and power < 75:
            power_alert_counter = 0
            voice.getAndPlay("Sistemas de potencia bajo control")
            homeware.setParam("rgb001", "color", store["rgb001"]["color"])
            homeware.setParam("rgb001", "on", store["rgb001"]["on"])

def systemVoiceReport(homeware, voice, topic, payload):
  if topic == "home" and payload == "systems_voice_report" \
    or topic == "device/scene_systems_report/deactivate" and not payload:
    not_pass = []
    if not homeware.getHomewareTest():
        not_pass.append("homeware")

    if len(not_pass) == 0:
        voice.getAndPlay("Todos los sistemas están operativos")
    elif len(not_pass) == 1:
        voice.getAndPlay(not_pass[0] + " no está operativo")
    else:
        text = "No están operativos los siguientes sistemas: "
        for i, system in enumerate(not_pass):
            if not i == len(not_pass) - 2:
                text += system + ", "
            else:
                text += system + " y "
        voice.getAndPlay(text)