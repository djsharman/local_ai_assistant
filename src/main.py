from audio_handler import record_audio
from src.whisper_handler import transcribe_audio
from llama_handler import get_llama_response
from piper_handler import text_to_speech, play_audio
from context_manager import initialize_db, save_context, load_context

def main():
    initialize_db()
    context = load_context()

    while True:
        record_audio("input.wav")
        user_text = transcribe_audio("input.wav")
        print(f"User said: {user_text}")

        context += f" {user_text}"
        response = get_llama_response(user_text, context)
        print(f"Llama3 Response: {response}")

        save_context(context)
        text_to_speech(response, "response.wav")
        play_audio("response.wav")

if __name__ == "__main__":
    main()
