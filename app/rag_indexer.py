import os
import shutil
import time
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

def clear_vector_db():
    """Safely clear the vector database directory"""
    db_path = "app/vector_db"
    if os.path.exists(db_path):
        print("🧹 Clearing previous vector database...")
        try:
            # Try normal deletion first
            shutil.rmtree(db_path)
        except PermissionError:
            print("⚠️ Couldn't delete immediately, retrying...")
            time.sleep(1)  # Wait for file handles to release
            try:
                shutil.rmtree(db_path)
            except Exception as e:
                print(f"❌ Couldn't clear directory: {e}")
                return False
        print("✅ Database cleared successfully")
    return True

def initialize_vector_db():
    if not clear_vector_db():
        return

    print("📥 Loading FA-tagged.txt")
    try:
        loader = TextLoader("resources/FA-tagged.txt", encoding="utf-8")
        documents = loader.load()
        print(f"📄 Loaded {len(documents)} documents")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return

    print("✂️ Splitting text into chunks")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"🔹 Total Chunks: {len(chunks)}")

    print("🤖 Loading local embedding model...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    print("💾 Creating vector store...")
    try:
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="app/vector_db",
            collection_name="first_aid",
            collection_metadata={
                "hnsw:space": "cosine",
                "persist": True
            }
        )
        print("✅ Vector DB created and persisted successfully!")
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")

if __name__ == "__main__":
    initialize_vector_db()