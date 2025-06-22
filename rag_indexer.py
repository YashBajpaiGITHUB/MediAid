from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Load first-aid PDF only
loader = PyMuPDFLoader("resources/FA-manual-YashProject.pdf")
documents = loader.load()

# Semantic chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75)
chunks = splitter.split_documents(documents)

# Use mpnet embeddings for deep match
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Save to vector DB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="app/vector_db"
)
db.persist()
print("✅ Vector DB created using PDF only.")
