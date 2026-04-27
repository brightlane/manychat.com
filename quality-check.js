const fs = require('fs');
const path = require('path');

const pagesDir = path.join(__dirname, 'pages');
const files = fs.readdirSync(pagesDir).filter(file => file.endsWith('.html'));

console.log("🧐 Running Quality Check...");

let errors = 0;
files.forEach(file => {
    const stats = fs.statSync(path.join(pagesDir, file));
    if (stats.size < 500) {
        console.log(`⚠️ Warning: ${file} seems too small (${stats.size} bytes).`);
        errors++;
    }
});

if (errors === 0) {
    console.log(`✅ Quality Check Passed: ${files.length} pages look healthy.`);
} else {
    console.log(`❌ Quality Check found ${errors} potential issues.`);
}
