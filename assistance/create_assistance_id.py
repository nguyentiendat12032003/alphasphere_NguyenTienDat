import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

payload = {
    "name": "OptiBot Helper",
    "instructions": "You are OptiBot, the customer-support bot for OptiSigns.com.Tone: helpful, factual, concise.Only answer using the uploaded docs.Max 5 bullet points else link to the doc, cite up to 3 Article URL: lines per reply.",
    
    "model": "gpt-4.1-mini",
    "tools": [
        { "type": "file_search" }
    ],
    "tool_resources": {
        "file_search": {
            "vector_store_ids": [VECTOR_STORE_ID]
        }
    }
}

response = requests.post("https://api.openai.com/v1/assistants", headers=headers, json=payload)

if response.ok:
    assistant = response.json()
    print("Assistant created successfully!")
    print("Assistant ID:", assistant["id"])
else:
    print("Failed to create assistant:", response.status_code)
    print(response.text)
