import google.generativeai as genai
import re
from typing import Tuple, List
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_subtopics(topic: str) -> List[str]:
    prompt = f"""
        You are a blog planning assistant. Your task is to generate a detailed outline for a long-form blog post based on the topic: "{topic}". 

        Output:
        1. A target audience in one line.
        2. A list of 5-7 clear, descriptive subheadings (in Markdown format using ##).

        Avoid giving multiple outlines. Stick to the best one.
        """

    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        subtopics = response.text.strip().split('\n')
        return [subtopic.strip() for subtopic in subtopics if subtopic]
    except Exception as e:
        print(f"[red]Error generating subtopics: {e}[/red]")
        return []


def get_audience(topic: str, tone: str) -> str:
    if tone == "educational":
        return "Beginners and students interested in learning about the topic."
    elif tone == "technical":
        return "Professionals and experts in the field."
    elif tone == "creative":
        return "Creative individuals and artists looking for inspiration."
    else:
        return "General audience interested in the topic."

def plan_topic(topic: str, tone: str = "educational") -> Tuple[List[str], str]:
    subtopics = get_subtopics(topic)
    if not subtopics:
        subtopics = ["Subtopic generation failed. Please try again."]
    audience = get_audience(topic, tone)
    return subtopics, audience

