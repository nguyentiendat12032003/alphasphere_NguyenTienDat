import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_vector_store(name="MyVectorStore"):
    url = "https://api.openai.com/v1/vector_stores"
    payload = {"name": name}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.ok:
        vs_id = response.json()["id"]
        print(f"Created vector store with ID: {vs_id}")
        return vs_id
    else:
        print("Failed to create vector store:", response.status_code)
        print(response.text)
        return None

if __name__ == "__main__":
    create_vector_store()