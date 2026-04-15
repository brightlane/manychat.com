import os
import sqlite3
import random
from datetime import datetime

DB = "seo.db"
OUTPUT_DIR = "pages"

AFFILIATE_LINKS = [
    "https://manychat.partnerlinks.io/bbwxetk27f88-64kfxo",
    "https://manychat.partnerlinks.io/98hj6b3pr28k-4znb59",
    "https://manychat.partnerlinks.io/emwcbue22i01-ogcg6e",
    "https://manychat.partnerlinks.io/t8let4hhqtqg-wki14",
    "https://manychat.partnerlinks.io/nwkkk7vkps17"
]

# ----------------------------
# DB CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# GET SEO OPPORTUNITIES
# ----------------------------
def get_build_keywords():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT keyword, impressions, clicks, ctr, position
        FROM queries
        WHERE impressions > 20
    """)

    rows = cur.fetchall()
    conn.close()

    keywords = []

    for r in rows:

        score = 0

        # Strong intent signals
        if r["impressions"] > 100:
            score += 2

        if r["position"] > 10:
            score += 3

        if r["ctr"] < 2:
            score += 2

        # Only build if meaningful opportunity
        if score >= 4:
            keywords.append(r["keyword"])

    # remove duplicates
    return list(set(keywords))

# ----------------------------
# CHECK IF PAGE EXISTS
# ----------------------------
def page_exists(keyword):
    slug = keyword.replace(" ", "-").lower()
    return os.path.exists(f"{OUTPUT_DIR}/{slug}.html")

# ----------------------------
# PICK AFFILIATE LINK
# ----------------------------
def get_affiliate_link():
    return random.choice(AFFILIATE_LINKS)

# ----------------------------
# GENERATE HTML PAGE
# ----------------------------
def build_page(keyword):

    slug = keyword.replace(" ", "-").lower()
    affiliate = get_affiliate_link()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{keyword}</title>
        <meta name="description" content="Learn about {keyword} and automation strategies.">
    </head>

    <body style="font-family:Arial;max-width:900px;margin:auto;padding:20px;">

        <h1>{keyword}</h1>

        <p>
            This page explains <strong>{keyword}</strong> and how businesses use automation tools to improve engagement and results.
        </p>

        <h2>Why this matters</h2>
        <p>
            Understanding {keyword} helps improve marketing efficiency, automation workflows, and customer engagement.
        </p>

        <h2>Recommended Tool</h2>
        <p>
            Many businesses use automation platforms to manage messaging, workflows, and conversions.
        </p>

        <a href="{affiliate}" target="_blank" rel="nofollow sponsored"
           style="display:inline-block;margin-top:20px;padding:10px 15px;background:#2563eb;color:white;text-decoration:none;border-radius:6px;">
            Try Automation Tool
        </a>

        <hr>

        <small>
            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </small>

    </body>
    </html>
    """

    return slug, html

# ----------------------------
# SAVE PAGE
# ----------------------------
def save_page(slug, html):

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    path = f"{OUTPUT_DIR}/{slug}.html"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[CREATED] {path}")

# ----------------------------
# MAIN ENGINE
# ----------------------------
def run():

    print("🚀 SEO GENERATOR STARTED")

    keywords = get_build_keywords()

    print(f"📊 Opportunities found: {len(keywords)}")

    created = 0
    skipped = 0

    for kw in keywords:

        if page_exists(kw):
            print(f"[SKIP] exists: {kw}")
            skipped += 1
            continue

        slug, html = build_page(kw)
        save_page(slug, html)

        print(f"[CREATED] {kw}")
        created += 1

    print("------------------------------------------------")
    print(f"DONE | CREATED: {created} | SKIPPED: {skipped}")

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    run()
