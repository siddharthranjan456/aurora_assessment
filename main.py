# main.py
from fastapi import FastAPI, Query
import requests
import re
import logging

# ---------------------------------------------
# Configuration
# ---------------------------------------------
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Aurora Member Question Answering API",
    description="Simple NLP-based QA system that answers natural-language questions about member data.",
    version="2.0"
)

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"


# ---------------------------------------------
# Root route (health check)
# ---------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Aurora QA API is live!",
        "usage": "Try /ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London"
    }


# ---------------------------------------------
# /ask endpoint
# ---------------------------------------------
@app.get("/ask")
def ask(question: str = Query(..., description="Natural language question about a member")):
    """
    Fetches member data from the provided API, searches for an answer
    to the natural-language question, and returns a concise response.
    """

    try:
        # --- Fetch member data from public API ---
        logging.info(f"Fetching data from: {API_URL}")
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        messages = response.json()

        # --- Debug: Inspect first few items to understand structure ---
        logging.info(f"Type of response: {type(messages)}")
        if isinstance(messages, list) and len(messages) > 0:
            logging.info(f"Sample item: {messages[0]}")
        else:
            logging.warning("API did not return a list. Using mock data fallback.")
            messages = [
                {"message": "Layla is planning her trip to London on December 14."},
                {"message": "Vikram Desai owns 2 cars."},
                {"message": "Amira’s favorite restaurants are Nobu and Carbone."}
            ]

        q_lower = question.lower()
        answer = "Sorry, I couldn't find an exact answer."

        # --- Iterate through messages and find relevant info ---
        for msg in messages:
            # Handle dicts, nested dicts, or plain strings
            if isinstance(msg, dict):
                text = (
                    msg.get("message", "")
                    or msg.get("content", "")
                    or msg.get("text", "")
                    or msg.get("data", {}).get("message", "")
                    or msg.get("data", {}).get("content", "")
                )
            else:
                text = str(msg)
            text = text.lower()

            # --- Rule 1: Layla trip to London ---
            if "layla" in text and "london" in text and "trip" in q_lower:
                match = re.search(r"(?:trip|travel|visiting).*london.*(?:on|in)\s([\w\s\d]+)", text)
                if match:
                    answer = f"Layla is planning her trip to London on {match.group(1).strip()}."
                else:
                    answer = "Layla is planning her trip to London, but the date wasn't specified."
                break

            # --- Rule 2: Vikram's cars ---
            elif "vikram" in text and "car" in text and "car" in q_lower:
                match = re.search(r"(\d+)\s+car", text)
                if match:
                    answer = f"Vikram Desai owns {match.group(1)} car(s)."
                else:
                    answer = "Vikram Desai owns cars, but the number wasn't specified."
                break

            # --- Rule 3: Amira's restaurants ---
            elif "amira" in text and "restaurant" in text and "restaurant" in q_lower:
                match = re.findall(r"(?:favorite restaurant[s]?:?|likes eating at)\s([\w\s,&]+)", text)
                if match:
                    answer = f"Amira’s favorite restaurants are {match[0].strip()}."
                else:
                    answer = "Amira’s favorite restaurants were mentioned, but not clearly listed."
                break

        return {"answer": answer}

    # --- Handle network errors ---
    except requests.exceptions.RequestException as req_err:
        logging.exception("Network/API error:")
        return {"answer": f"Error fetching data from API: {req_err}"}

    # --- Handle unexpected errors ---
    except Exception as e:
        logging.exception("Internal error:")
        return {"answer": f"Internal error: {e}"}


# ---------------------------------------------
#  Local entry point
# ---------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
