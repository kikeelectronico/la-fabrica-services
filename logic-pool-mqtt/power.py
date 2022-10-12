def powerManagment(homeware, topic, payload):
  print("hola")
  power = homeware.get("current001","brightness")
  print(power)