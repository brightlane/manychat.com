import os
import json
import random
from datetime import datetime

# =========================
# 🔗 AFFILIATE LINKS
# =========================
AFFILIATE_LINKS = [
    "https://manychat.partnerlinks.io/bbwxetk27f88-64kfxo",
    "https://manychat.partnerlinks.io/98hj6b3pr28k-4znb59",
    "https://manychat.partnerlinks.io/emwcbue22i01-ogcg6e",
    "https://manychat.partnerlinks.io/nwkkk7vkps17"
]

# =========================
# 🧠 VIRAL HOOKS
# =========================
HOOKS = [
    "Most people are doing Instagram marketing WRONG in 2026…",
    "This automation system is replacing manual DMs completely…",
    "You are losing leads every single day without this setup…",
    "AI chat funnels are changing how businesses make money…",
    "This is the simplest way to automate Instagram sales…"
]

# =========================
# 📄 LOAD KEYWORDS (FROM YOUR SEO SYSTEM)
# =========================
def load_keywords(file="keywords.txt"):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

# =========================
# 🔥 GENERATE SOCIAL POST
# =========================
def create_post(keyword):

    link = random.choice(AFFILIATE_LINKS)
    hook = random.choice(HOOKS)

    post_x = f"""
{hook}

Topic: {keyword}

Businesses are automating Instagram DMs using AI chat funnels.

No manual replies. No lost leads.

Start here:
{link}

#marketing #automation #ai #instagram
"""

    post_ig = f"""
🔥 {hook}

{keyword}

Turn Instagram into an automated sales machine using AI chat systems.

👉 {link}
"""

    post_linkedin = f"""
{keyword}

Modern marketing is shifting toward AI-driven conversational funnels.

Instead of manual outreach, businesses now automate lead generation.

Learn more:
{link}
"""

    return {
        "keyword": keyword,
        "created": datetime.now().isoformat(),
        "x": post_x,
        "instagram": post_ig,
        "linkedin": post_linkedin
    }

# =========================
# 💾 SAVE QUEUE
# =========================
def save_posts(posts):

    if not os.path.exists("social"):
        os.makedirs("social")

    path = "social/post_queue.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    print(f"Saved {len(posts)} social posts → {path}")

# =========================
# 📤 OPTIONAL AUTO-POST HOOK (API READY)
# =========================
def post_to_api(platform, content):
    """
    Placeholder for real API integration.

    X API / Meta Graph API / LinkedIn API go here.
    """

    print(f"[SIMULATED POST] {platform}:")
    print(content[:100], "...\n")

# =========================
# ⚙️ MAIN ENGINE
# =========================
def run():

    keywords = load_keywords()

    if not keywords:
        print("No keywords found.")
        return

    posts = []

    for kw in keywords[:20]:

        post = create_post(kw)
        posts.append(post)

    save_posts(posts)

    # OPTIONAL: simulate posting
    for p in posts[:3]:
        post_to_api("X", p["x"])
        post_to_api("Instagram", p["instagram"])
        post_to_api("LinkedIn", p["linkedin"])

    print("Social system complete.")


if __name__ == "__main__":
    run()
