import json

def payloadToBool(value):
  return value in ["True", "true"]

def loadPayload(payload):
  payload = payload.decode('utf-8').replace("\'", "\"")

  if payload in ["True", "true", "False", "false"]:
    return payload in ["True", "true"]
  elif "}" in payload or "]" in payload:
    return json.loads(payload)
  else:
    return payload