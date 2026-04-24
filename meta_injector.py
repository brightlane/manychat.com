import os
from bs4 import BeautifulSoup

# =========================
# 🌐 SITE CONFIG
# =========================
DOMAIN = "https://brightlane.github.io/manychat/"

SITE_NAME = "ManyChat Automation Hub"

DEFAULT_IMAGE = "https://via.placeholder.com/1200x630.png?text=ManyChat+Automation"

# =========================
# 🧠 META GENERATOR
# =========================
def build_meta(title, description, url):

    return f"""
<meta charset="UTF-8">

<title>{title}</title>

<meta name="description" content="{description}">
<meta name="robots" content="index, follow">

<link rel="canonical" href="{url}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DEFAULT_IMAGE}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{DEFAULT_IMAGE}">
"""

# =========================
# 🔧 INJECT INTO HTML
# =========================
def inject_meta(file_path):

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Get title fallback
    title = soup.title.string if soup.title else "ManyChat Guide"

    # Generate description fallback
    h1 = soup.find("h1")
    description = h1.text if h1 else "ManyChat automation guide for Instagram marketing."

    url = DOMAIN + os.path.basename(file_path)

    meta_tags = build_meta(title, description, url)

    # Inject into <head>
    if soup.head:
        soup.head.append(BeautifulSoup(meta_tags, "html.parser"))
    else:
        head_tag = soup.new_tag("head")
        head_tag.append(BeautifulSoup(meta_tags, "html.parser"))
        soup.html.insert(0, head_tag)

    # Save file back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print("Meta injected:", file_path)

# =========================
# ⚙️ BATCH PROCESSOR
# =========================
def run(folder="manychat"):

    if not os.path.exists(folder):
        print("Folder not found")
        return

    for file in os.listdir(folder):

        if file.endswith(".html"):
            inject_meta(os.path.join(folder, file))

    print("DONE - ALL PAGES OPTIMIZED")


if __name__ == "__main__":
    run()
