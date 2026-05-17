#!/usr/bin/env python3
"""
Uganda Tourism RAG PDF Generator
Interactive terminal app — pick a location, choose how many PDFs to generate.

Requirements:
  pip install groq reportlab

Usage:
  python generate_tourism_pdfs.py
"""

import os
import time
from pathlib import Path
from datetime import datetime

from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_JUSTIFY

LOCATIONS = [
    "Kidepo Valley National Park",
    "Murchison Falls National Park",
    "Gulu",
    "Sipi Falls",
    "Jinja",
    "Rwenzori Mountains",
    "Kibale National Park",
    "Kampala",
    "Queen Elizabeth National Park",
    "Entebbe",
    "Mbarara",
    "Lake Mburo National Park",
    "Lake Bunyonyi",
    "Kabale",
    "Bwindi Forest",
]

TOPICS = [
    {
        "id": "overview",
        "title": "Complete Visitor Guide",
        "prompt": (
            "Write a comprehensive visitor guide for {location}, Uganda. Cover:\n"
            "1. Introduction & Overview (history, significance, geography)\n"
            "2. Top Attractions & Must-See Highlights\n"
            "3. Best Time to Visit (seasons, weather, events)\n"
            "4. How to Get There (from Kampala and major hubs)\n"
            "5. Getting Around\n"
            "6. Accommodation Options (budget to luxury with examples)\n"
            "7. Local Cuisine & Dining\n"
            "8. Cultural Etiquette & Tips\n"
            "9. Safety & Health Precautions\n"
            "10. Practical Info (entry fees, opening hours, currency, connectivity)\n"
            "Be specific. Use ## for section headings and ### for subsections."
        ),
    },
    {
        "id": "wildlife_nature",
        "title": "Wildlife & Nature Guide",
        "prompt": (
            "Write a detailed wildlife and nature guide for {location}, Uganda. Cover:\n"
            "1. Flora & Fauna Overview (notable/endemic species with scientific names)\n"
            "2. Wildlife Viewing Tips (best spots and times)\n"
            "3. Birding Guide (key species and hotspots)\n"
            "4. Nature Trails & Hiking Routes (difficulty and duration)\n"
            "5. Conservation & Eco-Tourism\n"
            "6. Reputable Tour Operators\n"
            "7. Wildlife Photography Tips\n"
            "8. Seasonal Wildlife Calendar\n"
            "9. Responsible Viewing Guidelines\n"
            "Use ## for section headings and ### for subsections."
        ),
    },
    {
        "id": "activities",
        "title": "Activities & Adventures Guide",
        "prompt": (
            "Write a comprehensive activities and adventure guide for {location}, Uganda. Cover:\n"
            "1. Top Adventure Activities available at this location\n"
            "2. Cultural Experiences & Community Tourism\n"
            "3. Water-Based Activities (if applicable)\n"
            "4. Day Trips & Excursions\n"
            "5. Family-Friendly Activities\n"
            "6. Budget vs Premium Experiences (with approximate costs)\n"
            "7. Recommended Operators & Booking Tips\n"
            "8. What to Pack\n"
            "9. Fitness & Physical Requirements\n"
            "10. Permits & Booking Lead Times\n"
            "Use ## for section headings and ### for subsections."
        ),
    },
    {
        "id": "history_culture",
        "title": "History & Culture Guide",
        "prompt": (
            "Write a detailed history and culture guide for {location}, Uganda. Cover:\n"
            "1. Historical Background & Timeline\n"
            "2. Indigenous Communities & Tribes\n"
            "3. Traditional Customs, Ceremonies & Festivals\n"
            "4. Local Arts, Crafts & Music\n"
            "5. Notable Landmarks & Heritage Sites\n"
            "6. Colonial History & Independence\n"
            "7. Religious & Spiritual Sites\n"
            "8. Local Markets & Economic Life\n"
            "9. Famous People from the Area\n"
            "10. Tips for Culturally Respectful Travel\n"
            "Use ## for section headings and ### for subsections."
        ),
    },
    {
        "id": "food_dining",
        "title": "Food & Dining Guide",
        "prompt": (
            "Write a detailed food and dining guide for {location}, Uganda. Cover:\n"
            "1. Overview of Local Cuisine & Food Culture\n"
            "2. Must-Try Dishes & Street Foods\n"
            "3. Best Restaurants & Eateries (budget to upscale)\n"
            "4. Local Markets & Fresh Produce\n"
            "5. Vegetarian & Dietary Restriction Options\n"
            "6. Local Drinks & Beverages (including local brews)\n"
            "7. Food Safety Tips\n"
            "8. Cooking Classes & Food Tours\n"
            "9. Tipping Culture & Dining Etiquette\n"
            "10. Approximate Meal Costs\n"
            "Use ## for section headings and ### for subsections."
        ),
    },
]


def generate_content(client: Groq, location: str, topic: dict) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Uganda tourism writer with deep knowledge of "
                    "East African travel, geography, wildlife, and culture. "
                    "Write detailed, accurate, and engaging travel guide content. "
                    "Use markdown: ## for main sections, ### for subsections. "
                    "Be specific — include real place names, distances, price ranges, "
                    "and practical details wherever possible."
                ),
            },
            {
                "role": "user",
                "content": topic["prompt"].format(location=location),
            },
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()


def create_pdf(output_path: str, location: str, topic: dict, content: str):
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, spaceBefore=14, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=3)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14,
                          spaceAfter=5, alignment=TA_JUSTIFY)
    bullet_style = ParagraphStyle("bullet", parent=styles["Normal"], fontSize=10,
                                  leading=13, leftIndent=12, spaceAfter=2)

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"{location} - {topic['title']}",
    )

    story = []
    story.append(Paragraph(location, styles["Title"]))
    story.append(Paragraph(topic["title"], styles["Heading2"]))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %Y')}", styles["Normal"]))
    story.append(HRFlowable(width="100%", thickness=1))
    story.append(Spacer(1, 0.4*cm))

    for line in content.splitlines():
        s = line.strip()
        if not s:
            story.append(Spacer(1, 0.15*cm))
            continue

        safe = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        while "**" in safe:
            safe = safe.replace("**", "<b>", 1).replace("**", "</b>", 1)

        if safe.startswith("### "):
            story.append(Paragraph(safe[4:], h2))
        elif safe.startswith("## "):
            story.append(Paragraph(safe[3:], h1))
        elif safe.startswith("# "):
            story.append(Paragraph(safe[2:], h1))
        elif safe.startswith(("- ", "* ", "• ")):
            story.append(Paragraph(f"• {safe[2:]}", bullet_style))
        elif len(safe) > 1 and safe[0].isdigit() and safe[1] in ".)":
            story.append(Paragraph(safe, bullet_style))
        else:
            story.append(Paragraph(safe, body))

    doc.build(story)


def pick_location() -> str:
    print("\nLocations:")
    for i, loc in enumerate(LOCATIONS, 1):
        print(f"  {i:2}. {loc}")
    while True:
        raw = input("\nSelect location number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(LOCATIONS):
            return LOCATIONS[int(raw) - 1]
        print(f"  Enter a number between 1 and {len(LOCATIONS)}.")


def pick_num_docs() -> int:
    print(f"\nDocument types available ({len(TOPICS)}):")
    for i, t in enumerate(TOPICS, 1):
        print(f"  {i}. {t['title']}")
    while True:
        raw = input(f"\nHow many PDFs to generate? (1-{len(TOPICS)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(TOPICS):
            return int(raw)
        print(f"  Enter a number between 1 and {len(TOPICS)}.")


def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        api_key = input("Enter your Groq API key: ").strip()
    if not api_key:
        print("No API key provided. Exiting.")
        return

    client = Groq(api_key=api_key)

    # Kidepo and Murchison already done — skip them
    remaining = [loc for loc in LOCATIONS if loc not in (
        "Kidepo Valley National Park",
        "Murchison Falls National Park",
    )]

    output_dir = Path.home() / "Downloads" / "uganda_tourism_pdfs"
    num_docs = len(TOPICS)
    total = len(remaining) * num_docs
    done = 0

    print("=" * 40)
    print("  Uganda Tourism PDF Generator")
    print(f"  {len(remaining)} locations x {num_docs} PDFs = {total} total")
    print("=" * 40)

    for location in remaining:
        loc_slug = location.lower().replace(" ", "_").replace("/", "_")
        loc_dir = output_dir / loc_slug
        loc_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{location}]")
        for i, topic in enumerate(TOPICS, 1):
            done += 1
            print(f"  ({done}/{total}) {topic['title']} ...", end=" ", flush=True)
            try:
                content = generate_content(client, location, topic)
                fname = f"{loc_slug}_{i:02d}_{topic['id']}.pdf"
                create_pdf(str(loc_dir / fname), location, topic, content)
                print(f"saved -> {fname}")
            except Exception as e:
                print(f"error -> {e}")
            time.sleep(0.5)

    print(f"\nDone. All PDFs saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()