# Local AI Assistant

This project is a fully local AI assistant application that integrates speech recognition, natural language processing, and text-to-speech synthesis. The system listens to spoken input, processes it to text, generates a response using a language model, and then converts the response back to speech.

## Features

- **Speech Recognition**: Converts spoken words to text using Whisper.
- **Natural Language Processing**: Uses Llama3 via Ollama API to generate responses.
- **Text-to-Speech**: Converts text responses to speech using Piper.
- **Context Management**: Maintains a running conversation context, saved in an SQLite database.

## Setup Instructions

### Installation Steps

#### Clone the Repository

```bash
git clone https://github.com/djsharman/local_ai_assistant.git
cd local_ai_assistant
```
#### install Ollama here:
https://ollama.com/download

and install the llama3:8b model from here:
https://ollama.com/library/llama3

You can do the installation from your command line with this command:

```
ollama run llama3:8b
```


#### Download Required Models

Whisper Model: No extra steps needed; installed with the whisper package.
Piper Model: Download the ONNX model and JSON configuration file for Piper and place them in the appropriate directory.

```
wget -O en_US-joe-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx?download=true
wget -O en_US-joe-medium.onnx.json  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx.json?download=true.json
```

another voice you might like to try is here:

```
wget -O en_GB-northern_english_male-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx?download=true
wget -O en_GB-northern_english_male-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json?download=true
```

To switch voices you can change the line in piper_handler.py.

Also you can get alternative voices here:
https://github.com/rhasspy/piper/blob/master/VOICES.md

and you can try out all the voices piper supports here:
https://rhasspy.github.io/piper-samples/

#### create a virtual environment

```
python3 -m venv venv
```

#### install the dependencies

Activate the virtual environment

```
source ./venv/bin/activate
```

Do the required installations

```
pip install -r requirements.txt
```

## Run the Application

Activate the virtual environment. Only do this if you haven't already activated it during install.

```
source ./venv/bin/activate
```

Execute the main script to start the assistant.

```
python3 src/main.py
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bugs.

## License

This project is licensed under the MIT License.
