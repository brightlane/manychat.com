const fs = require('fs');
const path = require('path');

// Update this to the domain of the specific site
const BASE_URL = "https://your-manychat-site.com"; 

const pagesDir = path.join(__dirname, 'pages');
const files = fs.readdirSync(pagesDir).filter(file => file.endsWith('.html'));
const date = new Date().toISOString().split('T')[0];

let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${BASE_URL}/index.html</loc>
    <lastmod>${date}</lastmod>
    <priority>1.0</priority>
  </url>`;

files.forEach(file => {
    xml += `
  <url>
    <loc>${BASE_URL}/pages/${file}</loc>
    <lastmod>${date}</lastmod>
    <priority>0.8</priority>
  </url>`;
});

xml += `\n</urlset>`;

fs.writeFileSync('sitemap.xml', xml);
console.log(`✅ Sitemap generated for ${files.length} pages.`);
