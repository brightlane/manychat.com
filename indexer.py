import os
import sqlite3
from datetime import datetime

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
# INIT TABLE
# ----------------------------
def init_index_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS index_status (
        id INTEGER PRIMARY KEY,
        url TEXT,
        keyword TEXT,
        status TEXT,
        last_checked TEXT
    )
    """)

    conn.commit()
    conn.close()

# ----------------------------
# REGISTER PAGE
# ----------------------------
def register_page(url, keyword):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO index_status (url, keyword, status, last_checked)
    VALUES (?, ?, ?, ?)
    """, (
        url,
        keyword,
        "NOT_SUBMITTED",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

# ----------------------------
# SCAN GENERATED PAGES
# ----------------------------
def scan_pages():

    pages = os.listdir(PAGES_DIR)

    for file in pages:

        if not file.endswith(".html"):
            continue

        url = f"/pages/{file}"
        keyword = file.replace("-", " ").replace(".html", "")

        register_page(url, keyword)

        print(f"[REGISTERED] {url}")

# ----------------------------
# UPDATE STATUS (PLACEHOLDER FOR FUTURE API)
# ----------------------------
def update_status(url, status):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE index_status
    SET status = ?, last_checked = ?
    WHERE url = ?
    """, (
        status,
        datetime.now().isoformat(),
        url
    ))

    conn.commit()
    conn.close()

# ----------------------------
# RUN
# ----------------------------
def run():

    print("🚀 INDEXER STARTED")

    init_index_table()
    scan_pages()

    print("✅ INDEXING REGISTRY COMPLETE")

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    run()
