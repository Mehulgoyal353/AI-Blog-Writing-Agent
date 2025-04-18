import argparse
from writing_agent import generate_blog
from planner import plan_topic
from content_agent import fetch_content
from seo_agent import generate_seo_elements, generate_slug
from export_agent import export_blog, export_metadata
from rich.console import Console
from rich.table import Table
import asyncio

def main():
    # Initialize Console for rich output
    console = Console()

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Autonomous Blog Writing Agent")
    parser.add_argument("topic", type=str, help="Topic for the blog post (in quotes)")
    parser.add_argument("--tone", type=str, default="educational", help="Tone of the blog post (e.g., educational, casual, professional, etc.)")
    args = parser.parse_args()

    topic = args.topic
    tone = args.tone

    console.print(f"Starting the blog writing process for topic: {topic} with tone: {tone}", style="bold green")

    outline, audience = plan_topic(topic, tone)

    context = fetch_content(topic)

    blog_content = asyncio.run(generate_blog(topic, outline, tone, audience, context))


    seo_data = generate_seo_elements(topic, blog_content, tone)

    slug = generate_slug(topic)

    blog_path = export_blog(seo_data["title"], blog_content, slug)
    metadata_path = export_metadata(seo_data, topic, slug)

    console.print("[bold green]Blog writing process completed successfully![/bold green]")
    console.print("[bold blue]Here is the summary of the process:[/bold blue]")

    summary_table = Table(title="Blog Summary", show_lines=True)
    summary_table.add_column("Component", style="cyan", no_wrap=True)
    summary_table.add_column("Description", style="white")

    summary_table.add_row("Title", seo_data["title"])
    summary_table.add_row("Slug", slug)
    summary_table.add_row("Reading Time", f"{seo_data['reading_time']} minutes")
    summary_table.add_row("Meta Description", seo_data["meta_description"])
    summary_table.add_row("Tags", ", ".join(seo_data['keywords']))
    summary_table.add_row("Blog File", blog_path)
    summary_table.add_row("Metadata File", metadata_path)
    summary_table.add_row("Flesch-Kincaid Score", str(seo_data["flesch_kincaid_score"]))

    console.print(summary_table)

if __name__ == "__main__":
    main()
