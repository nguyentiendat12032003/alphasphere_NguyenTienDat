import os
import json
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

ARTICLES_DIR = "articles"
UPLOAD_LOG = "upload_log.json"
UPLOADED_FILES = []
TOTAL_CHUNKS = 0

# Split Markdown content into chunks (~500 tokens max), based on headings or length
def chunk_markdown(content):
    chunks = []
    current_chunk = ""
    for line in content.splitlines():
        if line.startswith("#") or len(current_chunk.split()) > 400:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

# Compute SHA256 hash of a file to detect content changes
def sha256_of_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# Load previous upload log to detect new or changed files
def load_upload_log():
    if os.path.exists(UPLOAD_LOG):
        with open(UPLOAD_LOG, "r") as f:
            return json.load(f)
    return {}

# Save upload log with file hash, chunk count, and file ID
def save_upload_log(log):
    with open(UPLOAD_LOG, "w") as f:
        json.dump(log, f, indent=2)

# Upload a file to OpenAI Files API with purpose="assistants"
def upload_file(filepath):
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        data = {"purpose": "assistants"}
        response = requests.post("https://api.openai.com/v1/files", headers=HEADERS, files=files, data=data)
        response.raise_for_status()
        return response.json()["id"]

# Attach uploaded file to a specified vector store with static chunking
def attach_file_to_vector_store(file_id):
    url = f"https://api.openai.com/v1/vector_stores/{VECTOR_STORE_ID}/files"
    payload = {
        "file_id": file_id,
        "chunking_strategy": {
            "type": "static",
            "static": {
                "max_chunk_size_tokens": 500,
                "chunk_overlap_tokens": 100
            }
        }
    }
    response = requests.post(
        url,
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload
    )
    if response.ok:
        print(f"Attached file {file_id} to vector store.")
        return True
    else:
        print(f"Failed to attach file {file_id}: {response.status_code}")
        print(response.text)
        return False

# Main function: detects new/updated files, uploads them, and attaches to vector store
def main():
    global TOTAL_CHUNKS
    upload_log = load_upload_log()

    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(ARTICLES_DIR, filename)
        file_hash = sha256_of_file(filepath)

        status = "new"
        if filename in upload_log:
            if upload_log[filename]["sha256"] == file_hash:
                print(f"⏭  Skipping {filename}: No changes.")
                continue
            else:
                status = "updated"

        print(f"\nUploading ({status.upper()}): {filename}")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_markdown(content)
        TOTAL_CHUNKS += len(chunks)

        try:
            file_id = upload_file(filepath)
            attached = attach_file_to_vector_store(file_id)
            if attached:
                UPLOADED_FILES.append(file_id)
                upload_log[filename] = {
                    "sha256": file_hash,
                    "file_id": file_id,
                    "chunks": len(chunks)
                }
                print(f"→ {filename} uploaded with {len(chunks)} chunks.")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

    save_upload_log(upload_log)
    print(f"\nDone. Uploaded {len(UPLOADED_FILES)} files, {TOTAL_CHUNKS} total chunks.")

if __name__ == "__main__":
    main()
