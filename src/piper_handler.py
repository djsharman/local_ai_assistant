from piper import PiperVoice
import wave  
from io import BytesIO
from pygame import mixer

mixer.init()


voice = PiperVoice.load('../en_US-ryan-medium.onnx', 
	config_path='../en_US-ryan-medium.onnx.json')

def text_to_speech(text):
    wavaudio = BytesIO()
    with wave.open(wavaudio, "wb") as wav_file:
        voice.synthesize(text, wav_file)
        wav_file.close()

    wavaudio.seek(0)

    mixer.music.load(wavaudio, "wav")
    mixer.music.play()

    # Wait until the playback has finished
    while mixer.music.get_busy():
        continue

