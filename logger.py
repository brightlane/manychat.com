import sqlite3
from datetime import datetime

DB = "seo.db"

# ----------------------------
# INIT LOG TABLE
# ----------------------------
def init_logs():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        event TEXT,
        detail TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# ----------------------------
# LOG EVENT
# ----------------------------
def log_event(event, detail=""):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO logs (event, detail, created_at)
    VALUES (?, ?, ?)
    """, (
        event,
        detail,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

# ----------------------------
# HELPERS
# ----------------------------
def log_created_page(keyword, slug):
    log_event("PAGE_CREATED", f"{keyword} -> {slug}")

def log_skipped(keyword, reason):
    log_event("SKIPPED", f"{keyword} | {reason}")

def log_cycle(status):
    log_event("CYCLE", status)


# ----------------------------
# INIT
# ----------------------------
if __name__ == "__main__":
    init_logs()
    print("Logs table ready")
