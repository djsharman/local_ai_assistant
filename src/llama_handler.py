import ollama
import json

def get_llama_response(prompt: str, json_context: list):

    print(f"Current JSON context: {json.dumps(json_context, indent=2)}")

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
