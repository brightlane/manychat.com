// 🔥 VULTURE QUALITY-CHECK.JS - 100% PREMIUM AUDIT
// Rejects low-quality pages, passes only Google EEAT-ready content
// Benny "Palmo Kid" - Langhorne SEO Empire

const fs = require('fs');
const path = require('path');

console.log('🚀 Starting Premium Quality Audit...');

const pageQualityStandards = {
  WORD_COUNT_MIN: parseInt(process.env.WORD_COUNT_MIN || '800'),
  INTERNAL_LINKS_MIN: parseInt(process.env.INTERNAL_LINKS_MIN || '10'),
  SCHEMA_REQUIRED: true,
  MOBILE_VIEWPORT: true,
  AFFILIATE_LINKS_MIN: 3,
  TITLE_UNIQUE: 50,  // Min chars for unique title
  READABILITY_TARGET: 70  // Flesch score
};

let totalPages = 0;
let passedPages = 0;
let rejectedPages = 0;
const rejected = [];

function calculateFleschScore(text) {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
  const words = text.split(/\s+/).filter(w => w.length > 3);
  const syllables = text.match(/[aeiouy]+/gi)?.length || 0;
  
  if (words.length === 0) return 0;
  const asl = words.length / sentences.length;
  const asw = syllables / words.length;
  return 206.835 - 1.015 * asl - 84.6 * asw;
}

function auditPage(filename) {
  try {
    const content = fs.readFileSync(filename, 'utf8');
    totalPages++;
    
    // 1. Word count (E-E-A-T depth)
    const words = content.split(/\s+/).length;
    
    // 2. Internal links
    const internalLinks = (content.match(/href="\/[^"]*\.html"/g) || []).length;
    
    // 3. Schema present
    const hasSchema = content.includes('schema.org') || content.includes('application/ld+json');
    
    // 4. Mobile viewport
    const hasViewport = content.includes('viewport') && content.includes('width=device-width');
    
    // 5. Affiliate ManyChat links
    const affiliateLinks = content.match(/manychat\.partnerlinks\.io/g)?.length || 0;
    
    // 6. Unique title
    const titleMatch = content.match(/<title[^>]*>(.*?)<\/title>/i);
    const titleLength = titleMatch ? titleMatch[1].trim().length : 0;
    
    // 7. Readability
    const bodyText = content.replace(/<[^>]*>/g, ' ').replace(/[^\w\s]/g, ' ');
    const fleschScore = calculateFleschScore(bodyText);
    
    // QUALITY GATE
    const passes = {
      words: words >= pageQualityStandards.WORD_COUNT_MIN,
      links: internalLinks >= pageQualityStandards.INTERNAL_LINKS_MIN,
      schema: hasSchema,
      mobile: hasViewport,
      affiliates: affiliateLinks >= pageQualityStandards.AFFILIATE_LINKS_MIN,
      title: titleLength >= pageQualityStandards.TITLE_UNIQUE,
      readability: fleschScore >= pageQualityStandards.READABILITY_TARGET
    };
    
    const allPass = Object.values(passes).every(Boolean);
    
    if (!allPass) {
      rejected.push({
        file: filename,
        fails: Object.keys(passes).filter(k => !passes[k]),
        words, internalLinks, titleLength, fleschScore
      });
      fs.unlinkSync(filename);
      rejectedPages++;
      return false;
    }
    
    passedPages++;
    console.log(`✅ PASS: ${filename} (${words} words, ${internalLinks} links)`);
    return true;
    
  } catch (error) {
    console.error(`❌ ERROR: ${filename} - ${error.message}`);
    rejectedPages++;
    return false;
  }
}

// MAIN AUDIT
const htmlFiles = fs.readdirSync('.')
  .filter(f => f.match(/\.html$/i) && !f.match(/^(index|sitemap|robots)/));

console.log(`🔍 Auditing ${htmlFiles.length} pages...`);

htmlFiles.forEach(auditPage);

console.log('\n📊 QUALITY REPORT:');
console.log(`Total: ${totalPages}`);
console.log(`✅ Passed: ${passedPages} (${((passedPages/totalPages)*100).toFixed(1)}%)`);
console.log(`❌ Rejected: ${rejectedPages}`);
console.log(`🚫 Low-quality files deleted: ${rejected.length}`);

if (rejected.length > 0) {
  console.log('\n🔍 Rejected details:');
  rejected.forEach(r => {
    console.log(`  ${r.file}: ${r.fails.join(', ')}`);
  });
}

if (passedPages === 0) {
  console.error('💥 CRITICAL: No pages passed quality! Check generator.');
  process.exit(1);
}

console.log('\n🎉 PREMIUM QUALITY AUDIT PASSED - Google EEAT Ready!');
console.log(`📈 Deploying ${passedPages} premium pages...`);
