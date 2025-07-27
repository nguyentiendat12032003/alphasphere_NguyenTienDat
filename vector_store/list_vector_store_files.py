import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def list_vector_store_files(vector_store_id, limit=100):
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}/files"
    params = {
        "limit": limit,
        "order": "desc"
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.ok:
        files = response.json().get("data", [])
        print(f"Vector store '{vector_store_id}' has {len(files)} files attached:")
        for file in files:
            print(f"- {file['id']} | {file.get('status')} | created_at: {file.get('created_at')}")
        return files
    else:
        print("Failed to list files:", response.status_code)
        print(response.text)
        return []

if __name__ == "__main__":
    list_vector_store_files(VECTOR_STORE_ID)
