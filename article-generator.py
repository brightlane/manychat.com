import random

def generate_related_links(current_page_id, total_pages=833):
    """Generates 5 random links to other vulture pages to keep the crawler moving."""
    related = []
    while len(related) < 5:
        rand_id = random.randint(1, total_pages)
        if rand_id != current_page_id:
            related.append(f'<li><a href="vulture-page-{rand_id}.html">ManyChat Strategy #{rand_id}</a></li>')
    return "".join(related)

# Example HTML snippet to inject into your 'vulture-page-X.html' template
internal_links_html = f"""
<div class="related-content" style="margin-top: 50px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
    <h3>Explore More ManyChat Automations</h3>
    <ul>
        {generate_related_links(current_id)}
    </ul>
</div>
"""
