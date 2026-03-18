from openai import OpenAI
from config import OPENAI_API_KEY

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_email(text):
    prompt = f"""
Summarize the following email in 2-3 clear sentences.
Do not hallucinate. Keep it factual.

Email:
{text[:1500]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()