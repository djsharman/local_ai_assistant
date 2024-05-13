import pyaudio
import wave
import time
import audioop

def record_audio(output_filename, silence_threshold=1000, silence_duration=3, sample_rate=16000, channels=1):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                         channels=channels,
                         rate=sample_rate,
                         input=True,
                         frames_per_buffer=1024)

    print("Recording... (start speaking)")

    frames = []
    recording = False
    silence_start_time = None

    while True:
        data = stream.read(1024)
        rms = audioop.rms(data, 2)  # Calculate RMS to detect silence

        if rms > silence_threshold:
            if not recording:
                recording = True
                print("Recording started...")
            frames.append(data)
            silence_start_time = None  # Reset silence timer
        else:
            if recording:
                if silence_start_time is None:
                    silence_start_time = time.time()
                else:
                    if time.time() - silence_start_time > silence_duration:
                        print("Recording completed")
                        break
               

        if recording:
            frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(output_filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(sample_rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
import sqlite3

def initialize_db():
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS context_history (
                        id INTEGER PRIMARY KEY,
                        context TEXT
                    )''')
    conn.commit()
    conn.close()

def save_context(context):
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO context_history (context) VALUES (?)", (context,))
    conn.commit()
    conn.close()

def load_context():
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute("SELECT context FROM context_history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
import ollama
import json

def get_llama_response(prompt: str, json_context: list):

    #print(f"Current JSON context: {json.dumps(json_context, indent=2)}")

    try:
        # Ensure all elements are properly formatted
        messages = [
            {"role": msg.get("role"), "content": msg.get("content")}
            for msg in json_context
            if isinstance(msg, dict) and "role" in msg and "content" in msg
        ]
    except Exception as e:
        print(f"Error in formatting messages: {e}")
        messages = []

    # Send JSON context to Ollama API
    response = ollama.chat(model='llama3', messages=messages)

    # Extract the response content
    result = response['message']['content']

    # Update the context with differentiated roles
    updated_context = json_context + [
        {"role": "assistant", "content": result}
    ]

    return result, updated_context
from audio_handler import record_audio
from whisper_handler import transcribe_audio
from llama_handler import get_llama_response
from piper_handler import text_to_speech
from context_manager import initialize_db, save_context, load_context
import json

def main():
    initialize_db()
    context = load_context()
    print(f"Startup context: {context}")

    # Prepare the initial JSON context with system messages
    INITIAL_CONTEXT = [
        {
            "role": "system",
            "content": "You are talking with a user. They are using a speech to text system to provide you with input. Understand that sometimes the tts system makes mistakes."
        },
        {
            "role": "system",
            "content": "Please keep your answers concise and to the point. Please do not embelish your output with anything that cannot be easily read out by a speech to text system. For example long list, or double asterisks."
        }
    ]

    # Load 
    json_context = INITIAL_CONTEXT.copy()
    if context:
        try:
            context_list = json.loads(context)  # Ensure context is properly parsed
            json_context.extend(context_list)
        except json.JSONDecodeError as e:
            print(f"Error decoding context JSON: {e}")
            context_list = []

    while True:
        record_audio("input.wav")
        user_text = transcribe_audio("input.wav")
        print(f"User said: {user_text}")



        json_context.append({
            "role": "user",
            "content": user_text
        })

        response, updated_context = get_llama_response(user_text, json_context)
        context = json.dumps(updated_context)  # Save updated context as a JSON string
        print(f"Llama3 Response: {response}")

        save_context(context)
        text_to_speech(response)

if __name__ == "__main__":
    main()
from piper import PiperVoice
import wave  
from io import BytesIO
from pygame import mixer

mixer.init()


voice = PiperVoice.load('../en_GB-northern_english_male-medium.onnx en_US-ryan-medium.onnx', 
	config_path='../en_US-ryan-medium.onnx.json')

#voice = PiperVoice.load('../en_GB-northern_english_male-medium.onnx', 
#	config_path='../en_GB-northern_english_male-medium.onnx')


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

import whisper
import torch


torch.cuda.init()
device = "cuda" # if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result['text']
