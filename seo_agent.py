import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
from utils.retry_helper import retry
from textstat.textstat import textstat

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def calculate_flesch_kincaid(content: str) -> float:
    return textstat.flesch_kincaid_grade(content)

@retry(max_attempts=3, delay=2, backoff=2)
def generate_title(topic: str, tone: str) -> str:
    prompt = f"Generate an SEO-friendly title for a blog post on: '{topic}', in a {tone} tone."
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

@retry(max_attempts=3, delay=2, backoff=2)
def generate_meta_description(topic: str, tone: str = "educational") -> str:
    prompt = f"Generate a 150 character SEO meta description for a blog post on: '{topic}', in a {tone} tone."
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

@retry(max_attempts=3, delay=2, backoff=2, exceptions=(requests.exceptions.RequestException,))
def get_keywords(topic: str) -> list:
    url = f"https://api.datamuse.com/words?ml={topic}&max=10"
    response = requests.get(url)
    response.raise_for_status()
    keywords = [word["word"] for word in response.json()]
    return keywords

def estimate_reading_time(content: str) -> str:
    words = len(content.split())
    reading_time = words / 200
    return f"{round(reading_time)} minutes"

def generate_slug(topic: str) -> str:
    slug = topic.lower().replace(" ", "-").replace(",", "").replace(".", "").replace("?", "")
    return slug

def generate_seo_elements(topic: str, content: str, tone: str = "educational") -> dict:
    title = generate_title(topic, tone)
    meta_description = generate_meta_description(topic, tone)
    keywords = get_keywords(topic)
    reading_time = estimate_reading_time(content)
    slug = generate_slug(topic)

    flesch_kincaid_score = calculate_flesch_kincaid(content)

    return {
        "title": title,
        "meta_description": meta_description,
        "keywords": keywords,
        "reading_time": reading_time,
        "slug": slug,
        "flesch_kincaid_score": flesch_kincaid_score 
    }
