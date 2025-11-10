Aurora Member Question Answering API

This project implements a simple Question-Answering API that can understand and answer natural-language questions about Aurora member data using the public /messages endpoint.

Overview
The service exposes one endpoint:

GET /ask?question=<your question>

You can ask questions such as:
- When is Layla planning her trip to London?
- How many cars does Vikram Desai have?
- What are Amira’s favorite restaurants?

The API fetches live data from Aurora’s public API, analyzes it, and returns an inferred answer.

Example Response
{ "answer": "Layla is planning her trip to London on December 14." }

How It Works
1. User asks a question through /ask
2. FastAPI app calls Aurora’s public endpoint at https://november7-730026606190.europe-west1.run.app/docs#/default/get_messages_messages__get
3. Responses are parsed from fields such as message, content, or text
4. Regex and keyword logic detects entities (Layla, Vikram, Amira) and their related facts
5. Answer is returned in JSON format.

Tech Stack
FastAPI - Build and serve the REST API
Requests - Fetch member data from the public API
Regex - Parse and extract answers from text
Uvicorn - Run the application server

Local Setup
1. Clone the repository
   git clone https://github.com/<your-username>/aurora-member-qa.git
   cd aurora-member-qa

2. Install dependencies
   pip install -r requirements.txt

3. Run locally
   python main.py
   or
   uvicorn main:app --reload

4. Open in browser
   Swagger UI: http://127.0.0.1:8000/docs
   Example query: http://127.0.0.1:8000/ask?question=What%20are%20Amira%27s%20favorite%20restaurants

Example Queries
When is Layla planning her trip to London?
Response: { "answer": "Layla is planning her trip to London on December 14." }

How many cars does Vikram Desai have?
Response: { "answer": "Vikram Desai owns 2 car(s)." }

What are Amira’s favorite restaurants?
Response: { "answer": "Amira’s favorite restaurants are Nobu and Carbone." }

API Reference
GET /ask
Parameter: question (string) - Natural-language question about a member
Response: { "answer": "..." }

GET / - Health check endpoint

Design Notes
Approach 1 – Regex and Keyword Matching (current)
Fast and simple but limited to known patterns.

Approach 2 – Semantic Search (Embedding-based)
Encodes text and compares similarity, better understanding of paraphrasing.

Approach 3 – Retrieval-Augmented LLM (RAG)
Uses GPT or Llama to interpret and answer flexibly, highest accuracy but higher cost.

Data Insights
The /messages endpoint may return inconsistent formats (message, content, text).
Some entries use nested data (data.content), others are plain strings.
Dates appear in various formats.
Regex may fail if structure changes.

Deployment
Deploy on Render or Railway.

Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 8000

Example public URL:
https://aurora-qa-service.onrender.com/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London

Requirements.txt
fastapi
uvicorn
requests

Author
Siddharth Ranjan
Email: Siddharth.ranjan2001@gmail.com
LinkedIn:- https://www.linkedin.com/in/mr-siddharth-ranjan/
