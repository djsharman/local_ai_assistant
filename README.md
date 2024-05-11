# Local AI Assistant

This project is a fully local AI assistant application that integrates speech recognition, natural language processing, and text-to-speech synthesis. The system listens to spoken input, processes it to text, generates a response using a language model, and then converts the response back to speech.

## Features

- **Speech Recognition**: Converts spoken words to text using Whisper.
- **Natural Language Processing**: Uses Llama3 via Ollama API to generate responses.
- **Text-to-Speech**: Converts text responses to speech using Piper.
- **Context Management**: Maintains a running conversation context, saved in an SQLite database.

## Setup Instructions

### Prerequisites

- **Python 3.9+**
- **Poetry** for package management

### Installation Steps

#### Clone the Repository
```bash
git clone https://github.com/djsharman/local_ai_assistant.git
cd local_ai_assistant
```


#### Install Poetry

Follow the instructions on the Poetry website to install Poetry on your system.
Example for Unix systems
```
curl -sSL https://install.python-poetry.org | python3 -
```

#### Install Dependencies
Use Poetry to install the project dependencies
```
poetry install
```

#### Activate the Virtual Environment
Activate the virtual environment created by Poetry.
```
poetry shell
```

#### Download Required Models

Whisper Model: No extra steps needed; installed with the whisper package.
Piper Model: Download the ONNX model and JSON configuration file for Piper and place them in the appropriate directory.

```
wget -P models/ https://path.to.your.model/en_US-lessac-medium.onnx
wget -P models/ https://path.to.your.model/en_US-lessac-medium.onnx.json
```

### Run the Application

Execute the main script to start the assistant.

```
poetry shell
python main.py
```

### Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bugs.

### License
This project is licensed under the MIT License.