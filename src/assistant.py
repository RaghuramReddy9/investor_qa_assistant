import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.router import route_question
from src.rag import ask_question as ask_from_vector
from src.live_tool import fetch_live_news


# Load environment variables
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    # api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


def clean_search_query(question: str) -> str:
    """
    Convert a user question into a clean search query for live APIs.
    """
    q = question.lower()
    stop_phrases = [
        "what is", "what are", "what happened", "what happened to",
        "latest", "current", "today", "this week", "news about"
    ]
    for phrase in stop_phrases:
        q = q.replace(phrase, "")
    return q.strip()


def answer_question(question: str) -> str:
    """
    Answer the user question using either static vector data
    or live external API data based on routing decision.
    """
    route = route_question(question)

    if route == "vector":
        return ask_from_vector(question)

    # live route
    search_query = clean_search_query(question)
    live_context = fetch_live_news(search_query)

    prompt = f"""
    You are an investor assistant.

    Using ONLY the live news context below, answer the user's question.
    If the context does not contain enough information, say:
    "I don't have enough live information to answer that."

    Live Context:
    {live_context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    while True:
        q = input("\nEnter your question (or 'exit' to quit): ")
        if q.lower() == "exit":
            break
        print("\nAnswer:\n", answer_question(q))
        