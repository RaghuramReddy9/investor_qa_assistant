import os
import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def fetch_live_news(query: str, max_articles: int=3) -> str:
    """
    Fetch recent news articles related to the query.
    Returns combined article text.
    """
    
    params = {
        "q" : f'"{query}"',
        "searchIn": "title,description",
        "launguage": "en",
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(NEWS_ENDPOINT, params=params, timeout=10)

    if response.status_code != 200:
        return "Could not fetch live news at the moment."
    
    data = response.json()
    articles = data.get("articles", [])

    # Adding Filter for quality articles
    filtered_articles = []
    query_lower = query.lower()

    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        if query_lower in text:
            filtered_articles.append(article)

    if not filtered_articles:
        filtered_articles = articles

    
    content = []
    for article in filtered_articles:
        title = article.get("title", "")
        description = article.get("description", "")
        content.append(f"Title: {title}\nDescription: {description}\n")

    return "\n".join(content)