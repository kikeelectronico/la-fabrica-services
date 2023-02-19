
class Alert:

  __mqtt_client = None
  __openai_client = None

  def __init__(self, mqtt_client, openai_client):
    self.__mqtt_client = mqtt_client
    self.__openai_client = openai_client

  def voice(self, input_text, gpt3=False):
    output_text = input_text
    if gpt3:
      openai_response = self.__openai_client.Completion.create(
        model="text-davinci-003",
        prompt="Dime una frase similar a: " + input_text,
        max_tokens=30,
        temperature=0.8
      )
      output_text = openai_response["choices"][0]["text"].replace("\n", "")
      print(output_text)
    self.__mqtt_client.publish("voice-alerts", output_text)

  def message(self, text):
    self.__mqtt_client.publish("message-alerts", text)