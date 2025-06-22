# ✅ app/agent.py

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
import urllib.parse
import requests

# ✅ Load the vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db = Chroma(
    persist_directory="app/vector_db",
    embedding_function=embedding_model
)

# ✅ Load Ollama (local model)
llm = Ollama(model="mistral")

# 🧠 Function to get first-aid response using retriever and local LLM
def get_first_aid_response(query: str) -> str:
    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""You are a certified medical assistant trained in first-aid.
You will be given an emergency situation. Based on the context, reply clearly and accurately.

Context:
{context}

Query:
{query}

Give a concise and clear first-aid solution."""

    response = llm.invoke(prompt)
    return response

def get_youtube_video_url(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query=first+aid+{urllib.parse.quote(query)}"
        response = requests.get(search_url)
        if "watch?v=" in response.text:
            start = response.text.find("watch?v=")
            end = response.text.find("\"", start)
            video_id = response.text[start:end].replace("watch?v=", "")
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"Video fetch error: {e}")
    return None

def get_google_maps_url(query):
    base = "https://www.google.com/maps/search/hospitals+near+"
    return base + urllib.parse.quote(query)
