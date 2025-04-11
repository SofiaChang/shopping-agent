import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .utils import QueryError


load_dotenv()

MODEL = "gemini-1.5-pro"

SYSTEM_INSTRUCTIONS = '''
    You are a shopping assistant. Users may speak in multiple steps.

    Your job is to maintain and update a structured JSON object representing the user's shopping filters. From the user's input, if vague, make the best prediction for the category that will be used to search for products.

    Each time the user sends a message, respond with a JSON object containing two keys:
    - `trigger_new_scrape` (bool): true if the filters were changed and a new product search should happen, false if the message doesn't significantly change the filters
    - `constraints`: update only the relevant fields in the JSON and return the full updated object. Preserve all other existing fields. The user may refer to previous values implicitly (e.g. "Actually, make it cheaper").

    Always return valid JSON in the following format:

    {
    "trigger_new_scrape": bool,
    "constraints": {
        "category": Optional[str],
        "min_price": Optional[float],
        "max_price": Optional[float],
        "prime_required": bool,
        "min_rating": Optional[float],
        "min_reviews": Optional[int]
    }
    }
    If a value is not mentioned or relevant, use null.
'''

class LLM:
    def __init__(self, prompt: str = ""):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = MODEL
        
        self.chat = self.client.chats.create(model=self.model, config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS),
        )

    def send_message(self, prompt: str):
        response = self.chat.send_message(prompt)
        if response.text:
            result = self.extract_json(response.text)
            print(f"Sofia Result: {result}")
            return result
        else:
            raise QueryError("Please try again, the agent is not responding.")
    
    def get_history(self):
        for message in self.chat.get_history():
            print(f'role - {message.role}',end=": ")
            print(message.parts[0].text)
        return self.chat.get_history()
    
    def extract_json(self, text: str) -> str:
        text = re.sub(r"^```json\s*|```$", "", text.strip(), flags=re.MULTILINE)
        return text.strip()