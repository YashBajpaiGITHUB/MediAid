from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.llms import Ollama
from langchain.embeddings.base import Embeddings  # Import base class
import urllib.parse
import requests
from typing import List

# ✅ Custom wrapper for SentenceTransformer
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text], show_progress_bar=False)[0].tolist()

# ✅ Instantiate embedding wrapper
embedding_function = SentenceTransformerEmbeddings()

# ✅ VectorDB setup
db = Chroma(
    persist_directory="app/vector_db",
    embedding_function=embedding_function
)

llm = Ollama(model="mistral")

# ✅ First-aid answer generator
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
import urllib.parse
import requests

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
