import os
import sqlite3
import random
from collections import defaultdict

DB = "seo.db"
PAGES_DIR = "pages"

# ----------------------------
# DB CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# GET ALL PAGES
# ----------------------------
def get_pages():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, keyword
        FROM page_performance
    """)

    rows = cur.fetchall()
    conn.close()

    return rows

# ----------------------------
# GROUP BY TOPIC (simple clustering)
# ----------------------------
def cluster_pages(pages):

    clusters = defaultdict(list)

    for p in pages:

        keyword = p["keyword"].lower()

        # simple clustering logic (can be upgraded later)
        if "chatbot" in keyword:
            clusters["chatbot"].append(p)
        elif "automation" in keyword:
            clusters["automation"].append(p)
        elif "marketing" in keyword:
            clusters["marketing"].append(p)
        else:
            clusters["general"].append(p)

    return clusters

# ----------------------------
# CREATE INTERNAL LINKS
# ----------------------------
def generate_links(cluster):

    links = []

    for page in cluster:

        url = page["url"]
        keyword = page["keyword"]

        # pick 2 random related pages in same cluster
        related = random.sample(cluster, min(2, len(cluster)))

        for r in related:

            if r["url"] == url:
                continue

            links.append({
                "from": url,
                "to": r["url"],
                "anchor": r["keyword"]
            })

    return links

# ----------------------------
# UPDATE HTML FILES
# ----------------------------
def inject_links(links):

    for link in links:

        try:
            file_path = link["from"].replace("/pages/", PAGES_DIR + "/")

            if not os.path.exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # simple injection point
            new_link = f'<a href="{link["to"]}">{link["anchor"]}</a>'

            if new_link not in content:
                content = content.replace(
                    "</body>",
                    f"<p>Related: {new_link}</p></body>"
                )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"[LINKED] {link['from']} → {link['to']}")

        except Exception as e:
            print(f"[ERROR] {link['from']} -> {e}")

# ----------------------------
# MAIN ENGINE
# ----------------------------
def run():

    print("🚀 INTERNAL LINKING STARTED")

    pages = get_pages()

    if not pages:
        print("No pages found")
        return

    clusters = cluster_pages(pages)

    all_links = []

    for name, cluster in clusters.items():

        if len(cluster) < 2:
            continue

        links = generate_links(cluster)
        all_links.extend(links)

    inject_links(all_links)

    print("------------------------------------------------")
    print(f"LINKS CREATED: {len(all_links)}")

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    run()
