from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB = "seo.db"

# ---------------------------
# CONNECT DATABASE
# ---------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# BUILD OPPORTUNITIES ENGINE
# ---------------------------
def get_build_opportunities():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT keyword, impressions, clicks, ctr, position
        FROM queries
        WHERE impressions > 50
    """)

    rows = cur.fetchall()
    conn.close()

    results = []

    for r in rows:
        score = 0

        if r["impressions"] > 100:
            score += 2
        if r["position"] > 10:
            score += 3
        if r["ctr"] < 2:
            score += 2

        if score >= 4:
            results.append({
                "keyword": r["keyword"],
                "score": score,
                "action": "BUILD"
            })

    return results

# ---------------------------
# CONTENT PROTECTION ENGINE
# ---------------------------
def get_protection_signals():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, keyword, clicks, impressions, ctr
        FROM pages
    """)

    rows = cur.fetchall()
    conn.close()

    signals = []

    for r in rows:

        risk = "SAFE"
        action = "NONE"

        # low CTR = optimization
        if r["ctr"] < 2:
            risk = "WEAK CTR"
            action = "OPTIMIZE TITLE"

        # high impressions but low clicks = mismatch
        if r["impressions"] > 100 and r["clicks"] == 0:
            risk = "INTENT MISMATCH"
            action = "REWRITE CONTENT"

        signals.append({
            "url": r["url"],
            "keyword": r["keyword"],
            "risk": risk,
            "action": action
        })

    return signals

# ---------------------------
# WINNER DETECTION ENGINE
# ---------------------------
def get_winners():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, clicks, impressions
        FROM pages
        WHERE clicks > 5
        ORDER BY clicks DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "url": r["url"],
            "status": "WINNER"
        }
        for r in rows
    ]

# ---------------------------
# MAIN API ENDPOINT
# ---------------------------
@app.route("/dashboard")
def dashboard():

    data = {
        "build_opportunities": get_build_opportunities(),
        "protection_layer": get_protection_signals(),
        "winners": get_winners()
    }

    return jsonify(data)

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
