import os
import sqlite3
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
# DB CONNECT
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# GET BUILD OPPORTUNITIES
# ----------------------------
def get_build_keywords():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT keyword, impressions, ctr, position
        FROM queries
        WHERE impressions > 50
    """)

    rows = cur.fetchall()
    conn.close()

    keywords = []

    for r in rows:
        score = 0

        if r["impressions"] > 100:
            score += 2
        if r["position"] > 10:
            score += 3
        if r["ctr"] < 2:
            score += 2

        if score >= 4:
            keywords.append(r["keyword"])

    return list(set(keywords))

# ----------------------------
# CHECK IF PAGE EXISTS
# ----------------------------
def page_exists(keyword):
    filename = f"{OUTPUT_DIR}/{keyword.replace(' ', '-')}.html"
    return os.path.exists(filename)

# ----------------------------
# AFFILIATE PICKER
# ----------------------------
def get_affiliate():
    import random
    return random.choice(AFFILIATE_LINKS)

# ----------------------------
# PAGE TEMPLATE GENERATOR
# ----------------------------
def build_page(keyword):

    affiliate = get_affiliate()
    slug = keyword.replace(" ", "-")

    html = f"""
    <html>
    <head>
        <title>{keyword} - Guide</title>
        <meta name="description" content="Learn about {keyword} and how to use automation tools effectively.">
    </head>
    <body style="font-family:Arial;max-width:800px;margin:auto;">

        <h1>{keyword}</h1>

        <p>
        This guide explains everything about <strong>{keyword}</strong> and how businesses use automation tools to improve results.
        </p>

        <h2>Why it matters</h2>
        <p>
        Automation is becoming essential for scaling communication, engagement, and lead generation.
        </p>

        <h2>Recommended tool</h2>
        <p>
        Many businesses use automation platforms to handle messaging and workflows.
        </p>

        <a href="{affiliate}" target="_blank" rel="nofollow sponsored">
            Try Automation Tool
        </a>

        <hr>
        <small>Generated: {datetime.now()}</small>

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
# MAIN RUNNER
# ----------------------------
def run():

    keywords = get_build_keywords()

    print(f"Found {len(keywords)} build opportunities")

    for kw in keywords:

        if page_exists(kw):
            print(f"[SKIP] already exists: {kw}")
            continue

        slug, html = build_page(kw)
        save_page(slug, html)

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    run()
