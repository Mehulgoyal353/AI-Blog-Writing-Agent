import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-1.5-flash")

async def generate_outline(topic: str, tone: str = "educational") -> list:
    prompt = f"""
        Generate a clear, logical outline (5–7 section headings) for a blog post on: "{topic}".
        - Tone: {tone}
        - Each heading should be descriptive and capable of supporting a full paragraph or two.
        - Avoid numbering. Don't include the introduction or conclusion — only main body headings.
        - Focus on clarity and technical relevance.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return [line.strip() for line in response.text.split('\n') if line.strip()]
    except Exception as e:
        print(f"[red]Error generating outline: {e}[/red]")
        return []

async def generate_intro(topic: str, tone: str = "educational") -> str:
    prompt = f"""
        Write an engaging introduction for a blog post on: "{topic}".
        - Tone: {tone}
        - Use a natural, informative tone.
        - Introduce the topic with some background or motivation.
        - Hook the reader; don't mention what will be covered.
        Length: 100–150 words.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[red]Error generating intro: {e}[/red]")
        return ""

async def generate_section(heading: str, topic: str, tone: str = "educational") -> str:
    prompt = f"""
        Write a detailed, 200-300 word section on the following subtopic: {heading}.
        The main topic is '{topic}', and the tone should be {tone}.
        Focus on content, not listing out subtopics.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[red]Error generating section: {e}[/red]")
        return ""

async def generate_conclusion(topic: str, tone: str = "educational") -> str:
    prompt = f"""
        Write a concluding paragraph for a blog post on the topic: "{topic}".
        - Tone: {tone}
        - Summarize key takeaways without repeating section headings.
        - Optionally end with a reflective comment or call-to-action.
        Length: ~100–150 words.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[red]Error generating conclusion: {e}[/red]")
        return ""

async def generate_blog(topic: str, outline: list, tone: str, audience: str, context: dict) -> str:
    intro_task = asyncio.create_task(generate_intro(topic, tone))
    conclusion_task = asyncio.create_task(generate_conclusion(topic, tone))

    section_tasks = [generate_section(heading, topic, tone) for heading in outline]
    sections = await asyncio.gather(*section_tasks)

    intro = await intro_task
    conclusion = await conclusion_task

    blog_md = f"# {topic}\n\n{intro}\n\n"

    for heading, content in zip(outline, sections):
        blog_md += f"## {heading}\n\n{content}\n\n"

    blog_md += f"## Conclusion\n\n{conclusion}\n\n"
    return blog_md
