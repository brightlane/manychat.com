import os
from openai import OpenAI

# =========================
# 🔑 OPENAI SETUP
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# CONFIG
# =========================
OUTPUT_DIR = "manychat"
KEYWORD_FILE = "keywords.txt"

DOMAIN = "https://brightlane.github.io/manychat/"

AFFILIATE_LINKS = [
    "https://manychat.partnerlinks.io/bbwxetk27f88-64kfxo",
    "https://manychat.partnerlinks.io/98hj6b3pr28k-4znb59",
    "https://manychat.partnerlinks.io/emwcbue22i01-ogcg6e",
    "https://manychat.partnerlinks.io/nwkkk7vkps17"
]

# =========================
# 🧠 PROMPT ENGINE
# =========================
def generate_article(keyword):
    prompt = f"""
You are an expert SEO copywriter.

Write a HIGH-QUALITY 1500–2000 word SEO article about:

"{keyword}"

Requirements:
- Professional SaaS marketing tone
- Focus on ManyChat automation, Instagram DM funnels, AI marketing
- Include headings (H2, H3)
- Include step-by-step explanations
- Include conversion psychology
- Natural flow (no keyword stuffing)
- Must feel like a real marketing guide

Include this concept:
- ManyChat automation as core tool for {keyword}

Do NOT mention that you are AI.

Return only HTML body content (no <html>, no <head>).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =========================
# 💰 CTA BLOCK
# =========================
def cta_block(link):
    return f"""
    <div style="margin:30px 0;padding:20px;background:#f4f7ff;border-left:5px solid #0073ff;">
        <h3>🚀 Start Automating Your Business</h3>
        <p>Use ManyChat to turn Instagram traffic into automated sales funnels.</p>
        <a href="{link}" style="background:#0073ff;color:white;padding:12px 18px;text-decoration:none;border-radius:6px;">
            👉 Launch Automation System
        </a>
    </div>
    """


# =========================
# 📄 HTML WRAPPER
# =========================
def build_page(keyword, content, link):

    slug = keyword.lower().replace(" ", "-") + ".html"
    path = os.path.join(OUTPUT_DIR, slug)

    html = f"""
<!DOCTYPE html>
<html>

<head>
<title>{keyword} | ManyChat SEO Guide</title>

<meta name="description" content="Learn {keyword} using AI automation and ManyChat funnels.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{DOMAIN}{slug}">

<style>
body {{
    font-family: Arial;
    max-width: 900px;
    margin: auto;
    padding: 20px;
    line-height: 1.7;
}}
</style>

</head>

<body>

<h1>{keyword}</h1>

{cta_block(link)}

{content}

{cta_block(link)}

</body>
</html>
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return slug


# =========================
# ⚙️ MAIN ENGINE
# =========================
def run():

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(KEYWORD_FILE):
        print("Missing keywords.txt")
        return

    with open(KEYWORD_FILE, "r") as f:
        keywords = [k.strip() for k in f if k.strip()]

    for kw in keywords[:20]:

        print(f"Generating: {kw}")

        content = generate_article(kw)
        link = AFFILIATE_LINKS[0]

        build_page(kw, content, link)

    print("DONE - AI ARTICLES GENERATED")


if __name__ == "__main__":
    run()
