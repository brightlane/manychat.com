import os
import random
import re
from datetime import datetime

# Setup the root URL for this specific project
BASE_URL = "https://brightlane.github.io/manychat"

def generate_tree_content(kw):
    intros = [
        f"Mastering the {kw} flow within ManyChat is essential for 2026 growth.",
        f"How to build a high-conversion {kw} ecosystem.",
        f"The technical guide to {kw} automation."
    ]
    return f"<p>{random.choice(intros)}</p><p>This page is part of the <strong>ManyChat Authority Tree</strong>.</p>"

def main():
    # 1. Create the 'pages' directory for the 10k keywords
    if not os.path.exists('pages'):
        os.makedirs('pages')
    
    # 2. Load keywords
    keywords = ["Chatbot Marketing"] # Default
    if os.path.exists('keywords.txt'):
        with open('keywords.txt', 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]

    # 3. Generate the 10k keyword pages
    for kw in keywords[:5000]:
        body = generate_tree_content(kw)
        safe_name = re.sub(r'[^a-zA-Z0-9\s-]', '', kw.lower()).strip().replace(' ', '-')
        
        with open(f"pages/{safe_name}.html", 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>{kw} | ManyChat Authority</title>
    <style>body{{font-family:sans-serif; max-width:800px; margin:auto; padding:50px; line-height:1.6;}}</style>
</head>
<body>
    <nav><a href="{BASE_URL}/index.html">🏠 ManyChat Home</a></nav>
    <h1>{kw}</h1>
    {body}
    <hr>
    <footer>Auto-Sync: {datetime.now().strftime('%Y-%m-%d')}</footer>
</body>
</html>""")

    print(f"✅ Created {len(keywords[:5000])} branches in the ManyChat tree.")

if __name__ == "__main__":
    main()
