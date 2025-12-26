import os
from google.genai import Client
import json
import re

def extract_topic_phrases(review_text: str) -> list[str]:
    """
    Extract topic phrases using Gemini API and return list of short phrases.
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Gemini API key missing.")
        return []

    client = Client(api_key=api_key)

    prompt = f"""
    Extract core customer concern topics from the review below.
    Return a JSON list of short phrases (max 4 words each).

    Review:
    "{review_text}"
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        text = response.text.strip()

        # remove code block formatting if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:-1]
            text = "\n".join(lines).strip()

        # try to parse JSON
        try:
            items = json.loads(text)
            if isinstance(items, list):
                cleaned = []
                for phrase in items:
                    if isinstance(phrase, str) and phrase.strip():
                        phrase = re.sub(r'[^\w\s]', '', phrase).lower().strip()
                        cleaned.append(phrase)
                return cleaned
        except Exception:
            pass

        # fallback: line-based extraction
        phrases = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            line = re.sub(r'^[\d\-\•\*\.\s]+', '', line).strip()
            line = re.sub(r'[^\w\s]', '', line).lower().strip()
            if len(line.split()) <= 6:
                phrases.append(line)

        return phrases

    except Exception as e:
        print(f"Error extracting topics: {e}")
        return []
