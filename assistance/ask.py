import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID= os.getenv("ASSISTANCE_ID")

print("Loaded Assistant ID:", ASSISTANT_ID)


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

def create_thread():
    response = requests.post(
        "https://api.openai.com/v1/threads",
        headers=HEADERS
    )
    return response.json()["id"]

def send_message(thread_id, content):
    payload = {
        "role": "user",
        "content": content
    }
    response = requests.post(
        f"https://api.openai.com/v1/threads/{thread_id}/messages",
        headers=HEADERS,
        json=payload
    )
    return response.json()["id"]

def run_assistant(thread_id):
    payload = {
        "assistant_id": ASSISTANT_ID
    }
    response = requests.post(
        f"https://api.openai.com/v1/threads/{thread_id}/runs",
        headers=HEADERS,
        json=payload
    )
    if not response.ok:
        print("Failed to run assistant:")
        print(response.status_code)
        print(response.text)
        return None
    run_id = response.json()["id"]
    print("▶Run ID:", run_id)
    return run_id

def wait_for_completion(thread_id, run_id):
    while True:
        response = requests.get(
            f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
            headers=HEADERS
        )
        run_info = response.json()
        status = run_info["status"]
        print("Run status:", status)
        if status in ["completed", "failed", "cancelled", "expired"]:
            if "last_error" in run_info and run_info["last_error"]:
                print("Last error:", run_info["last_error"])
            return status
        time.sleep(2)


def get_response(thread_id):
    response = requests.get(
        f"https://api.openai.com/v1/threads/{thread_id}/messages",
        headers=HEADERS
    )
    messages = response.json()["data"]
    for m in messages:
        if m["role"] == "assistant":
            print("Assistant response:")
            print(m["content"][0]["text"]["value"])
            return

if __name__ == "__main__":
    thread_id = create_thread()
    send_message(thread_id, "How do I add a YouTube video?")
    run_id = run_assistant(thread_id)
    wait_for_completion(thread_id, run_id)
    get_response(thread_id)
