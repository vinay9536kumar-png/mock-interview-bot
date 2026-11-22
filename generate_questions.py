import time
from xmlrpc import client
from xmlrpc import client
from google.genai import errors

MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]


def call_gemini(prompt, retries=4):
    for attempt in range(retries):
        for model in MODELS:
            try:
                return client.models.generate_content(
                    model=model, contents=prompt
                ).text
            except errors.ServerError:
                continue
        time.sleep(2 ** attempt)  # 1s, 2s, 4s, 8s
    raise RuntimeError("Gemini अभी busy है, थोड़ी देर बाद try करो")