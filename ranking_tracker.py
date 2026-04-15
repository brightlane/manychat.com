import sqlite3
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, date

DB = "seo.db"
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# ----------------------------
# DB CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# INIT PERFORMANCE TABLE
# ----------------------------
def init_table():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS page_performance (
        id INTEGER PRIMARY KEY,
        url TEXT,
        keyword TEXT,
        clicks INTEGER,
        impressions INTEGER,
        ctr REAL,
        position REAL,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# ----------------------------
# GOOGLE SEARCH CONSOLE SERVICE
# ----------------------------
def get_service():

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    return build("searchconsole", "v1", credentials=creds)

# ----------------------------
# FETCH GSC DATA
# ----------------------------
def fetch_data(service, site_url):

    request = {
        "startDate": str(date.today().replace(day=1)),
        "endDate": str(date.today()),
        "dimensions": ["page", "query"],
        "rowLimit": 25000
    }

    response = service.searchanalytics().query(
        siteUrl=site_url,
        body=request
    ).execute()

    return response.get("rows", [])

# ----------------------------
# SAVE PERFORMANCE
# ----------------------------
def save(rows):

    conn = get_db()
    cur = conn.cursor()

    for r in rows:

        page = r["keys"][0]
        keyword = r["keys"][1]

        clicks = r.get("clicks", 0)
        impressions = r.get("impressions", 0)
        ctr = r.get("ctr", 0)
        position = r.get("position", 0)

        cur.execute("""
        INSERT INTO page_performance (
            url, keyword, clicks, impressions, ctr, position, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            page,
            keyword,
            clicks,
            impressions,
            ctr,
            position,
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()

# ----------------------------
# ANALYZE WINNERS + LOSERS
# ----------------------------
def analyze():

    conn = get_db()
    cur = conn.cursor()

    # Winners
    cur.execute("""
        SELECT url, clicks, impressions
        FROM page_performance
        WHERE clicks > 5
        ORDER BY clicks DESC
    """)
    winners = cur.fetchall()

    # Weak pages
    cur.execute("""
        SELECT url, impressions, ctr
        FROM page_performance
        WHERE impressions > 50 AND ctr < 0.02
    """)
    weak = cur.fetchall()

    conn.close()

    return winners, weak

# ----------------------------
# MAIN RUNNER
# ----------------------------
def run(site_url):

    print("🚀 RANKING TRACKER STARTED")

    init_table()

    service = get_service()
    rows = fetch_data(service, site_url)

    print(f"📊 Rows fetched: {len(rows)}")

    save(rows)

    winners, weak = analyze()

    print("------------------------------------------------")
    print(f"🏆 WINNERS: {len(winners)}")
    print(f"⚠️ WEAK PAGES: {len(weak)}")

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    SITE_URL = "https://yourdomain.com"
    run(SITE_URL)
