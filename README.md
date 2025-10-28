
# MediAid — First‑Aid RAG Assistant

## 🚀 Overview
**MediAid** is a Streamlit application that provides **concise first‑aid guidance** using a **Retrieval‑Augmented Generation (RAG)** workflow. It indexes an **official first‑aid PDF manual** into a local **Chroma** vector store (with **mpnet** embeddings) and uses a local **Ollama** LLM (**mistral**) to generate grounded, succinct responses for user queries. The app can also fetch a related **YouTube tutorial** and lets you **download** the advice as a **PDF**.

> ⚕️ **Medical disclaimer:** This tool is for **educational/assistance** purposes only. It does **not** replace professional medical advice. In emergencies, call your local emergency number.

---

## 🧩 Features
- 🧠 **RAG pipeline** over `resources/FA-manual-YashProject.pdf` (semantic search with Chroma + all‑mpnet‑base‑v2).
- 💬 **LLM generation** via **Ollama (mistral)** — runs locally/offline once the model is pulled.
- 🎥 **YouTube helper**: Finds a tutorial link for the entered first‑aid query (simple HTML scraping).
- 🧾 **Export**: Creates a one‑page PDF of the advice using **FPDF** with a download link in the UI.
- 📦 **Pre‑persisted vector DB** included (`app/vector_db/chroma.sqlite3`) for instant startup.

---

## 🏗️ Architecture (Code‑level)
- **UI**: `app/main.py` (launched by `streamlit_app.py`)
  - Text input for the emergency situation
  - Calls `get_first_aid_response(query)`
  - Shows optional YouTube link and “Nearby hospitals” page
  - Exports advice to PDF via **FPDF**
- **RAG Indexing**: `rag_indexer.py` (and `app/rag_indexer.py` utility variant)
  - Loads `resources/FA-manual-YashProject.pdf` with **PyMuPDF**
  - Splits text with **RecursiveCharacterTextSplitter** (`chunk_size=500`, `chunk_overlap=75`)
  - Embeds with **sentence-transformers/all-mpnet-base-v2**
  - Stores vectors in **Chroma** at `app/vector_db/`
- **Core logic**: `app/agent.py`
  - Initializes Chroma (persisted) with an embedding wrapper over **SentenceTransformer**
  - Sets up **Ollama(model="mistral")**
  - `get_first_aid_response(query)`: retrieves **k=4** chunks and builds a concise prompt
  - `get_youtube_video_url(query)`: scrapes YouTube results for a video id

**Primary stack**: `streamlit`, `langchain` (+ `langchain_community`), `chromadb`, `sentence_transformers`, `pymupdf`, `fpdf`, `requests`, `Ollama`

---

## 📁 Project Structure
The inner project folder is the real root. If your unzip shows a nested folder, **cd into the inner `MediAid-main/`** first.

```

```

Key paths:
- `app/main.py` — Streamlit UI
- `app/agent.py` — RAG + LLM helpers (`get_first_aid_response`, `get_youtube_video_url`)
- `rag_indexer.py` — Rebuilds vector DB from the PDF
- `resources/` — First‑aid PDF and derived text files (`FA-cleaned.txt`, `FA-tagged.txt`)
- `app/vector_db/` — Persisted Chroma DB (`chroma.sqlite3` included)

---

## ✅ Prerequisites
- **Python** 3.10/3.11 recommended
- **Ollama** installed locally and the **mistral** model pulled:
  ```bash
  ollama pull mistral
  ```
- OS packages required by **PyMuPDF** (if building from source) — typically handled via `pip` wheels on major platforms.

---

## 🛠️ Installation
From the **inner** `MediAid-main/` directory:

```bash
# 1) (Recommended) create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Running the App
Option A (repo shim):
```bash
python streamlit_app.py
```
This simply runs:
```python
streamlit run app/main.py
```

Option B (direct):
```bash
streamlit run app/main.py
```

Open the URL shown in your terminal (usually http://localhost:8501). Enter an emergency scenario, e.g., _“minor burn on hand”_. You should receive a concise, grounded response. Use the **Download** link to save a PDF of the advice.

> ℹ️ The repository already includes a persisted Chroma DB at `app/vector_db/` so you can start immediately.

---

## 🔁 Re‑indexing the Knowledge Base (Optional)
If you update or replace the manual PDF (`resources/FA-manual-YashProject.pdf`), regenerate the vector DB:

```bash
python rag_indexer.py
# This re-creates the Chroma store in app/vector_db/
```

Indexing details (from code):
- Loader: **PyMuPDF**
- Splitter: **RecursiveCharacterTextSplitter** (`chunk_size=500`, `chunk_overlap=75`)
- Embeddings: **sentence-transformers/all-mpnet-base-v2**
- Store: **Chroma** (`persist_directory="app/vector_db"`)

---

## 🔒 Privacy & Offline Mode
- The RAG pipeline (PDF → embeddings → retrieval) runs **fully offline**.
- With **Ollama** and the **mistral** model downloaded, generation is also offline.  
- External calls only occur if you **open the YouTube link** or **Maps** page.

---

## 🧪 Manual QA Hints
- Try queries like: “**minor cut on finger**”, “**sprain ankle**”, “**burn injury**”
- Verify the **Download as PDF** link appears after a response.
- Confirm that responses reflect content from the manual.

---

## 🤝 Contributing
- Please format with standard Python tooling (e.g., `black`, `ruff`).
- Propose improvements via PRs: better prompts, safer output structure (Do/Don’t, Red Flags, when to call emergency), multilingual support, or map helper fixes.

---

## 📄 License
License is **not specified** in this project archive. 

---

## 🧾 Credits
- First‑aid manual stored at `resources/FA-manual-YashProject.pdf`.
- Built with Streamlit, Chroma, Sentence Transformers, LangChain, PyMuPDF, FPDF, and Ollama.
