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
