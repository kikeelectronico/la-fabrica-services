from google.cloud import texttospeech
import threading
import os

from gtts import gTTS

DEVICES_IPS = ['192.168.10.15', '192.168.10.16', '192.168.10.17']

class Voice:

  def __init__(self):
    self.text_to_speech_client = texttospeech.TextToSpeechClient()
    self.voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES", name="es-ES-Wavenet-D", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    self.audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=1.2
    )
    #pass

  def getFile(self, text):
        file_name = text
        for c in ((" ", ""),("ó","o"),(".", ""),("á", "a"),("é", "e"),("í", "i"),("ú", "u"),("!", ""),("¡", ""),("?", ""),("¿", "")):
            file_name = file_name.replace(*c)
        file_path = "audio/" + file_name+".mp3"

        if os.path.exists(file_path):
            print("Already exists")
        else:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            response = self.text_to_speech_client.synthesize_speech(
                input=synthesis_input, voice=self.voice, audio_config=self.audio_config
            )

            with open(file_path, "wb") as out:
                out.write(response.audio_content)
        
            # t2s = gTTS(text=text, tld="es", lang='es', slow=False) 
            # t2s.save(file_path)

        return file_path

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

  def getAndPlay(self, text):
      file_path = self.getFile(text)
      self.playFile(file_path)