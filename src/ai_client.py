# ai_client.py
import os
import re
from openai import OpenAI
import json
from tenacity import retry, stop_after_attempt, wait_fixed

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def generate_content(prompt: str) -> dict:
    # Call endpoint with new syntax
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )
    
    raw = resp.choices[0].message.content
    # Print to console for debugging
    print("\n--- RAW MODEL OUTPUT ---")
    print(raw)
    print("--- END RAW ---\n")

    # Remove any code fences (```json or ```)
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()
    
    #text = resp.choices[0].message.content.strip()
    return parse_json(cleaned)

def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Malformed JSON: {e}")
