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
