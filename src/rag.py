import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

VECTOR_STORE_DIR = "storage/faiss"

def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )
    return FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

def build_prompt():
    template = """
    You are an investor assistant.
    Answer the question using ONLY the context below.
    If the answer is not present in the context, say "I don't have enough information."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

def ask_question(question: str):
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    docs = retriever._get_relevant_documents(question, run_manager=None)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = build_prompt().format(
        context=context,
        question=question
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=API_KEY,
        temperature=0
    )

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        answer = ask_question(q)
        print("\nAnswer:\n", answer)
