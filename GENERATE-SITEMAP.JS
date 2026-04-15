// 🔥 GENERATE-SITEMAP.JS - VULTURE 20K SEO POWER
// Benny "Palmo Kid" - Perfect Google/Bing/Yandex indexing
// Generates sitemap.xml with all 833 vulture pages

const fs = require('fs');
const path = require('path');

console.log('🚀 Generating Vulture Sitemap...');

try {
  // Build sitemap with all generated pages
  let sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://yourdomain.com/</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>`;

  // Add all vulture pages
  const pageFiles = fs.readdirSync('.')
    .filter(f => /^vulture-page-\d+\.html$/.test(f))
    .sort();

  pageFiles.forEach(filename => {
    const pageNum = filename.match(/vulture-page-(\d+)\.html/)[1];
    sitemap += `
  <url>
    <loc>/vulture-page-${pageNum}.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>`;
  });

  sitemap += `
</urlset>`;

  // Write sitemap
  fs.writeFileSync('sitemap.xml', sitemap);
  
  console.log(`✅ SITEMAP CREATED:`);
  console.log(`   📄 Total URLs: ${pageFiles.length + 1}`);
  console.log(`   🌐 Homepage + ${pageFiles.length} vulture pages`);
  console.log(`   📈 Daily crawl priority - Google loves it!`);
  console.log(`   💾 Saved: sitemap.xml`);

} catch (error) {
  console.log('⚠️  Sitemap partial - continuing workflow');
  // Create minimal sitemap as fallback
  fs.writeFileSync('sitemap.xml', `<?xml version="1.0"?><urlset><url><loc>/</loc></url></urlset>`);
  console.log('✅ Minimal sitemap created');
}

// Add robots.txt
const robots = `User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml`;
fs.writeFileSync('robots.txt', robots);
console.log('✅ robots.txt created with sitemap link');

console.log('\n🎉 SEO INFRASTRUCTURE COMPLETE');
console.log('🚀 Ready for GitHub Pages / Netlify / Vercel deployment');
