# ai_validation.py
import os
from openai import OpenAI
from templates import tpl

# Initialize the client once
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_fully_localized(text: str, locale: str) -> bool:
    """
    Ask the LLM if the `text` is written exclusively in the
    language associated with `locale`. Returns True if it is so.
    """
 
    
    
    validation_prompt = tpl.module.validate_language(locale,text)


    resp = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": validation_prompt}],
        temperature=0,
        max_tokens=3
    )

    answer = resp.choices[0].message.content.strip().lower()
    return answer.startswith("yes")

def check_title_length(title: str, max_len: int = 60) -> bool:
    """Tittle is longer that max_len."""
    return len(title) <= max_len

def check_body_contains_keyword(body: str, keyword: str) -> bool:
    """body contains the keyword (case-insensitive)."""
    return keyword.lower() in body.lower()