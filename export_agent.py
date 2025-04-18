import os
import json
from datetime import datetime

os.makedirs("blogs", exist_ok=True)
os.makedirs("metadata", exist_ok=True)

def export_blog(title: str, content: str, slug: str) -> str:
    filename = f"{slug}.md"
    filepath = os.path.join("blogs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)

    return filepath

def export_metadata(seo_data: dict, topic: str, slug: str) -> str:
    metadata = {
        "topic": topic,
        "title": seo_data["title"],
        "meta_description": seo_data["meta_description"],
        "keywords": seo_data["keywords"],
        "reading_time": seo_data["reading_time"],
        "slug": seo_data["slug"],
        "timestamp": datetime.utcnow().isoformat()
    }

    filename = f"{slug}.json"
    filepath = os.path.join("metadata", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    return filepath

def print_cli_summary(title: str, slug: str, reading_time: str, md_path: str, json_path: str):
    print("\n[bold green]Blog generated successfully![/bold green]")
    print(f"Title: {title}")
    print(f"Slug: {slug}")
    print(f"Reading Time: {reading_time}")
    print(f"Blog saved to: {md_path}")
    print(f"Metadata saved to: {json_path}")
