import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def call_llm(prompt: str) -> str:
    """
    Call Gemini API with a simple prompt.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    return response.text

def call_llm_with_history(messages: list) -> str:
    """
    Call Gemini API with conversation history.
    messages should be a list of {"role": "user"/"model", "parts": "..."}
    Note: Gemini uses "model" instead of "assistant" for the AI responses
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Convert messages to Gemini format if needed
    gemini_messages = []
    for msg in messages:
        if msg["role"] == "assistant":
            # Convert assistant to model for Gemini
            gemini_messages.append({"role": "model", "parts": msg["content"]})
        elif msg["role"] == "user":
            gemini_messages.append({"role": "user", "parts": msg["content"]})
        else:
            # Already in correct format
            gemini_messages.append(msg)
    
    chat = model.start_chat(history=gemini_messages[:-1])  # All but last message as history
    response = chat.send_message(gemini_messages[-1]["parts"])  # Send last message
    
    return response.text

if __name__ == "__main__":
    # Test the API call
    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable")
    else:
        test_prompt = "Hello, how are you?"
        response = call_llm(test_prompt)
        print(f"Test successful. Response: {response}")
