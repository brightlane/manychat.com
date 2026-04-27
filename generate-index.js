const fs = require('fs');
const path = require('path');

// Pull the site name from an env variable or default it
const siteName = "ManyChat Automation Directory";
const pagesDir = path.join(__dirname, 'pages');

try {
    // Read all generated pages
    const files = fs.readdirSync(pagesDir)
        .filter(f => f.endsWith('.html'))
        .sort((a, b) => {
            return parseInt(a.match(/\d+/)) - parseInt(b.match(/\d+/));
        });

    // Create the HTML links for the grid
    const linksHtml = files.map(file => {
        const id = file.match(/\d+/);
        return `<li><a href="pages/${file}">ManyChat Strategy #${id}</a></li>`;
    }).join('\n');

    const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${siteName}</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; padding: 40px; max-width: 1100px; margin: auto; background: #fff; }
        h1 { color: #007bff; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin-top: 30px; }
        ul { list-style: none; padding: 0; }
        li a { text-decoration: none; color: #333; font-size: 14px; display: block; padding: 8px; border: 1px solid #eee; border-radius: 4px; }
        li a:hover { background: #007bff; color: white; border-color: #007bff; }
    </style>
</head>
<body>
    <h1>🚀 ${siteName}</h1>
    <p>Select a strategy below to scale your automation workflows.</p>
    <ul class="grid">
        ${linksHtml}
    </ul>
</body>
</html>`;

    fs.writeFileSync('index.html', indexHtml);
    console.log(`✅ Index created successfully with ${files.length} strategy links.`);
} catch (err) {
    console.error("❌ Error generating index:", err.message);
    process.exit(1);
}
