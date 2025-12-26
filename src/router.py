from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv 
import os 


load_dotenv()


def route_question(question: str) -> str:
    """
    Decide whether the question needs static (vector) data
    or live (external API) data.
    Returns: 'vector' or 'live'
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    prompt = f"""
    you are a routing assistant.

    classify the user question into on catogory.
    - vector : if the question can be answered using general, static knowledge.
    - live : if the question depends on recent, current or real-time information.

    Return only one word: vector or live.

    Question: {question}
    Answer:
    """

    response = llm.invoke(prompt)
    return response.content.strip().lower()