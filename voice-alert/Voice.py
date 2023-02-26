from google.cloud import texttospeech
import threading
import os

DEVICES_IPS = ['192.168.10.15', '192.168.10.16', '192.168.10.17']

class Voice:

  def __init__(self):
    self.text_to_speech_client = texttospeech.TextToSpeechClient()
    self.voice = texttospeech.VoiceSelectionParams(
      language_code="es-ES",
      name="es-ES-Neural2-F"
    )
    self.audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=1.2
    )

  # Genereate mp3 file if needed
  def getFile(self, text):
    # Create file name
    file_name = text
    for c in ((" ", ""),("ó","o"),(".", ""),("á", "a"),("é", "e"),("í", "i"),("ú", "u"),("!", ""),("¡", ""),("?", ""),("¿", "")):
        file_name = file_name.replace(*c)
    file_path = "audio/" + file_name+".mp3"
    # If the mp3 file doesn't exists
    if not os.path.exists(file_path):
        # Get the speech binary from Google TTS
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.text_to_speech_client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        # Create the mp3 file
        with open(file_path, "wb") as out:
            out.write(response.audio_content)
    return file_path

  # Stream the mp3 to the smart speakers
  def playFile(self, file_path):
    class runCommandThread(threading.Thread):
        def __init__(self, command):
            threading.Thread.__init__(self)
            self.cmd = command

        def run(self):
            os.system(self.cmd)

    threads = []
    for ip in DEVICES_IPS:
        threads.append(runCommandThread("catt -d " + ip + " cast " + file_path))
        threads[-1].start()

  # Play an announcement
  def getAndPlay(self, text):
      file_path = self.getFile(text)
      self.playFile(file_path)