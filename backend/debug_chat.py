import os
from pageindex import PageIndexClient
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")

if not PAGEINDEX_API_KEY:
    # Use dummy for structure check if no key, but sdk might fail on auth
    print("No API Key found, may fail auth")
    
client = PageIndexClient(api_key=PAGEINDEX_API_KEY or "dummy")

query = "Hello"
file_ids = ["mock_id"] 

print("Attempting chat_completions with correct param...")
try:
    messages = [{"role": "user", "content": query}]
    # Using 'doc_id' as found in inspection
    try:
        response = client.chat_completions(
            messages=messages,
            doc_id=file_ids
        )
        print("chat_completions success:", response)
    except Exception as e:
        print(f"chat_completions failed with API error (expected if key/id invalid): {e}")

except Exception as e:
    print(f"chat_completions failed with Code error: {e}")
