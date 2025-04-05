
class Alert:

  __mqtt_client = None
  __openai_client = None

  def __init__(self, mqtt_client, openai_client, logger):
    self.__mqtt_client = mqtt_client
    self.__openai_client = openai_client
    self.logger = logger

  # Send a voice alert
  def voice(self, input_text, speaker="", gpt3=False):
    output_text = input_text
    # Process the message using GPT3 if required
    if gpt3:
      openai_response = self.__openai_client.Completion.create(
        model="text-davinci-003",
        prompt=input_text,
        max_tokens=256,
        temperature=1
      )
      output_text = openai_response["choices"][0]["text"].replace("\n", "")
    # Send the message
    self.__mqtt_client.publish("voice-alert/speakers", speaker)
    self.__mqtt_client.publish("voice-alert/text", output_text)

  # Send a message alert
  def message(self, text):
    self.__mqtt_client.publish("message-alerts", text)