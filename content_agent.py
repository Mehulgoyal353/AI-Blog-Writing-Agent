import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_news(topic: str, language: str = 'en', country: str = 'in') -> list:
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={topic}&language={language}&country={country}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("results", [])
        # return [article["title"] + " - " + article.get("link", "") for article in articles[:5]]
        return [article["title"] for article in articles[:3] if "title" in article]
    except Exception as e:
        print(f"[red]Error fetching news articles: {e} [/red]")
        return []

def fetch_keywords(topic: str) -> list:
    url = f"https://api.datamuse.com/words?ml={topic}&max=10"
    try:
        response = requests.get(url)
        response.raise_for_status()
        keywords = [word["word"] for word in response.json()]
        return keywords
    except Exception as e:
        print(f"[red]Error fetching keywords: {e} [/red]")
        return []
    
import requests

def fetch_quotes(topic: str) -> list:
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [f'"{data[0]["q"]}" - {data[0]["a"]}']
    except Exception as e:
        print(f"[red]Error fetching quotes: {e} [/red]")
        return []

def count_tokens(text: str):
    return len(text.split())

def fetch_content(topic: str) -> dict:
    return {
        "news": fetch_news(topic),
        "keywords": fetch_keywords(topic),
        "quotes": fetch_quotes(topic)
    }
