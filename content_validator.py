# ai_validation.py
import os
from openai import OpenAI

# Initialize the client once
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_fully_localized(text: str, locale: str) -> bool:
    """
    Ask the LLM if the `text` is written exclusively in the
    language associated with `locale`. Returns True if it is so.
    """
    # Simple mapping from locale to language name for the prompt
    lang_map = {
        "en_US": "English",
        "nl_NL": "Dutch",
        "pt_BR": "Portuguese",
        # add more locales if needed
    }
    target_language = lang_map.get(locale)
    # If en_US, we assume it's always in English
    if locale == "en_US" or not target_language:
        return True

    # Build the validation prompt
    validation_prompt = (
        f"I need you to check that the following text is written "
        f"100% in {target_language}, with no words, phrases, or sentences "
        f"in any other language. "
        f"Answer only 'yes' or 'no'.\n\n"
        f"---\n"
        f"{text}\n"
        f"---"
    )

    resp = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": validation_prompt}],
        temperature=0,
        max_tokens=3
    )

    answer = resp.choices[0].message.content.strip().lower()
    return answer.startswith("yes")

def check_title_length(title: str, max_len: int = 60) -> bool:
    """Title no más largo que max_len."""
    return len(title) <= max_len

def check_body_contains_keyword(body: str, keyword: str) -> bool:
    """body contiene la keyword (case-insensitive)."""
    return keyword.lower() in body.lower()