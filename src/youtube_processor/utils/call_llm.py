import anthropic
import os
from dotenv import load_dotenv
import itertools

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
api_keys = [
    os.getenv("ANTHROPIC_API_KEY"),
    os.getenv("ANTHROPIC_API_KEY_backup")
]
# Filter out any keys that are not set
api_keys = [key for key in api_keys if key]

if not api_keys:
    raise ValueError("No Anthropic API keys found. Please set ANTHROPIC_API_KEY or ANTHROPIC_API_KEY_backup environment variables.")

# Create a cycle iterator for the keys
key_cycler = itertools.cycle(api_keys)

def get_next_api_key():
    """Cycles through the available API keys."""
    return next(key_cycler)

def call_llm(prompt: str) -> str:
    """
    Call Anthropic Claude API with a simple prompt.
    Rotates through available API keys.
    """
    api_key = get_next_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def call_llm_with_history(messages: list) -> str:
    """
    Call Anthropic Claude API with conversation history.
    Rotates through available API keys.
    messages should be a list of {"role": "user"/"assistant", "content": "..."}
    Note: Anthropic uses "assistant" for AI responses (standard format)
    """
    api_key = get_next_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    
    # Convert messages to Anthropic format if needed
    anthropic_messages = []
    for msg in messages:
        if msg["role"] == "model":
            # Convert Gemini "model" to "assistant" for Anthropic
            anthropic_messages.append({"role": "assistant", "content": msg.get("parts", msg.get("content", ""))})
        elif msg["role"] == "user":
            content = msg.get("parts", msg.get("content", ""))
            anthropic_messages.append({"role": "user", "content": content})
        elif msg["role"] == "assistant":
            # Already in correct format
            anthropic_messages.append({"role": "assistant", "content": msg["content"]})
        else:
            # Default handling
            anthropic_messages.append(msg)
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=anthropic_messages
    )
    
    return response.content[0].text

if __name__ == "__main__":
    # Test the API call
    if not api_keys:
        print("Please set ANTHROPIC_API_KEY or ANTHROPIC_API_KEY_backup environment variable")
    else:
        test_prompt = "Hello, how are you?"
        response = call_llm(test_prompt)
        print(f"Test successful. Response: {response}")
