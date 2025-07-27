# alphasphere_NguyenTienDat
## Project Structure
```
├── articles/
├── assistance/
    ├── ask.py
    ├── create_assistant.py
├── scrape/
    ├── scrape_articles.py
├── vector_store/                               
    ├── create_vector_store.py       
    ├── upload_attach.py       
    ├── list_vector_store_files.py 
├── dockerfile       
├── requirements.txt                   
├── .env.sample                
└── README.md                  
```
##  Setup & Installation
1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-cryptic-repo-name.git
   cd your-cryptic-repo-name
   ```

2. **Create `.env` file from template:**
   ```bash
   cp .env.sample .env
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run scripts locally (example):**
   ```bash
   python upload_vectorstore.py
   python ask_question.py
   ```
---

## `.env.sample` Structure

```env
OPENAI_API_KEY=sk-...
VECTOR_STORE_ID=vs_...
ASSISTANT_ID=asst_...
```

## Method 1 – Using OpenAI Dashboard UI

Steps:

1. **Create a Vector Store on OpenAI platform dashboard.**

2. **Upload .md files using drag-and-drop.**

3. **OpenAI automatically performs chunking and embedding.**

4. **Create an Assistant by selecting model, system prompt, and linking the vector store.**

5. **Run a test query in Playground (e.g., "How do I add a YouTube video?").**

**Limitation:**
- Assistants created via UI cannot be controlled via API.
- <img width="1912" height="1075" alt="Screenshot 2025-07-23 142708" src="https://github.com/user-attachments/assets/77958492-5c1d-41bf-8345-470beb871c51" />


## Method 2 – Using Python & OpenAI API


1. **Prepare Markdown Files**

2. **Place support documents (e.g. .md files) in the articles/ folder.
Upload Files via API**
**Use the upload_to_vectorstore.py script.**

**Each file is uploaded via the https://api.openai.com/v1/files endpoint.**

**Files are then attached to a Vector Store via the https://api.openai.com/v1/vector_stores/{id}/files endpoint.**
<img width="1211" height="895" alt="Screenshot 2025-07-24 112234" src="https://github.com/user-attachments/assets/6f9385c6-66b6-4580-b360-da4dabb69994" />

3. **Chunking Configuration
**
Uses OpenAI's default static chunking:
```json
{
  "type": "static",
  "static": {
    "max_chunk_size_tokens": 600,
    "chunk_overlap_tokens": 100
  }
}
```
Rationale:
- max_chunk_size_tokens = 600: Each chunk contains up to 600 tokens (~450–500 words), providing sufficient context for accurate retrieval and response generation.
- chunk_overlap_tokens = 100: Ensures overlap between chunks to preserve semantic continuity across sections.
This balance minimizes the number of chunks while retaining context, improving both performance and quality of responses during assistant retrieval.
4. **Create Assistant**
The created Assistant is configured with:
```bash
https://api.openai.com/v1/assistants
```
Vector Store ID
System Prompt:
```
You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
```
5. **Ask Questions via API**
<img width="1226" height="506" alt="Screenshot 2025-07-24 112621" src="https://github.com/user-attachments/assets/48262946-53a7-417c-a703-b85cbed2206b" />

Use the ask_question.py script.

Steps:

- Create a thread (/v1/threads)
```bash
https://api.openai.com/v1/threads
```

Send a message (/v1/threads/{id}/messages)
```bash
https://api.openai.com/v1/threads/{thread_id}/messages
```
Trigger a run (/v1/threads/{id}/runs)
```bash
https://api.openai.com/v1/threads/{thread_id}/runs
```
Poll for completion and fetch result
