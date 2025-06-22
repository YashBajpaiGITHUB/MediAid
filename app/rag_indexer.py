from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

print("📥 Loading FA-tagged.txt")
loader = TextLoader("resources/FA-tagged.txt", encoding="utf-8")
documents = loader.load()
print(f"📄 Loaded {len(documents)} documents")

print("✂️ Splitting text into chunks")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75)
chunks = splitter.split_documents(documents)
print(f"🔹 Total Chunks: {len(chunks)}")

print("🤖 Loading local embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("💾 Creating vector store...")
db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="app/vector_db",
    collection_name="first_aid",
    # 👇 This ensures persistence on creation
    collection_metadata={"persist": True}
)

print("✅ Vector DB created and persisted.")
