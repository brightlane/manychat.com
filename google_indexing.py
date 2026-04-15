import sqlite3
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

DB = "seo.db"
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

# ----------------------------
# DB CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# GET PAGES TO INDEX
# ----------------------------
def get_pages():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, keyword
        FROM index_status
        WHERE status = 'NOT_SUBMITTED'
        LIMIT 50
    """)

    rows = cur.fetchall()
    conn.close()

    return rows

# ----------------------------
# GOOGLE INDEXING CLIENT
# ----------------------------
def get_service():

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    service = build("indexing", "v3", credentials=credentials)
    return service

# ----------------------------
# SUBMIT URL
# ----------------------------
def submit_url(service, url):

    body = {
        "url": url,
        "type": "URL_UPDATED"
    }

    request = service.urlNotifications().publish(body=body)
    response = request.execute()

    return response

# ----------------------------
# UPDATE STATUS IN DB
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
# MAIN RUNNER
# ----------------------------
def run():

    print("🚀 GOOGLE INDEXING STARTED")

    pages = get_pages()

    print(f"📄 Pages to submit: {len(pages)}")

    service = get_service()

    success = 0
    failed = 0

    for p in pages:

        url = p["url"]

        try:
            response = submit_url(service, url)
            update_status(url, "SUBMITTED")

            print(f"[SUBMITTED] {url}")
            success += 1

        except Exception as e:
            print(f"[FAILED] {url} -> {e}")
            update_status(url, "FAILED")
            failed += 1

    print("------------------------------------------------")
    print(f"DONE | SUCCESS: {success} | FAILED: {failed}")

# ----------------------------
# EXECUTE
# ----------------------------
if __name__ == "__main__":
    run()
