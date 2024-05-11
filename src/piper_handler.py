import subprocess

def text_to_speech(text, output_filename):
    command = f'echo "{text}" | ./piper --model en_US-lessac-medium.onnx --output_file {output_filename}'
    subprocess.run(command, shell=True)

def play_audio(file_path):
    subprocess.run(["aplay", file_path])
