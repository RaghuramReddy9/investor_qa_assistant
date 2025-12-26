import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

DATA_DIR = "data/documents"
VECTOR_STORE_DIR = "storage/faiss"

def load_documents():
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80
    )
    return splitter.split_documents(documents)

def build_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_DIR)

def main():
    print("Loading documents...")
    documents = load_documents()

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)

    print("Creating embeddings and vector store...")
    build_vector_store(chunks)

    print("Vector store created successfully.")

if __name__ == "__main__":
    main()
