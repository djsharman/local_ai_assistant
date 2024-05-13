import whisper
import torch


torch.cuda.init()
device = "cuda" # if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result['text']
