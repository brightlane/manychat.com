const fs = require("fs");
const path = require("path");

// ----------------------------
// CONFIG
// ----------------------------
const OUTPUT_DIR = path.join(__dirname, "pages");

// 🔥 HARD LIMIT (controlled by GitHub Actions)
const PAGE_LIMIT = parseInt(process.env.PAGE_LIMIT_PER_RUN || "20");

// Affiliate links from GitHub Actions env
const AFFILIATES = [
  process.env.AFFILIATE_1,
  process.env.AFFILIATE_2,
  process.env.AFFILIATE_3,
  process.env.AFFILIATE_4,
  process.env.AFFILIATE_5,
].filter(Boolean);

// ----------------------------
// KEYWORDS SOURCE
// Replace later with GSC / DB / scraper
// ----------------------------
function getKeywords() {
  return [
    "instagram automation tools",
    "how to grow instagram fast",
    "manychat chatbot guide",
    "best marketing automation tools",
    "ai marketing tools 2026",
    "lead generation strategies",
    "social media automation guide",
    "chatbot marketing explained",
    "content automation workflow",
    "digital marketing tools list"
  ];
}

// ----------------------------
// BASIC QUALITY FILTER
// ----------------------------
function isValidKeyword(keyword) {
  if (!keyword) return false;
  if (keyword.length < 5) return false;
  return true;
}

// ----------------------------
// ROTATE AFFILIATE LINKS
// ----------------------------
let affiliateIndex = 0;

function getAffiliateLink() {
  if (AFFILIATES.length === 0) return "#";

  const link = AFFILIATES[affiliateIndex % AFFILIATES.length];
  affiliateIndex++;

  return link;
}

// ----------------------------
// GENERATE HTML PAGE
// ----------------------------
function generateHTML(keyword) {
  const affiliate = getAffiliateLink();

  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${keyword}</title>
  <meta name="description" content="Learn about ${keyword}">
</head>
<body>

  <h1>${keyword}</h1>

  <p>
    This page explains <strong>${keyword}</strong> in a clear, structured way.
  </p>

  <h2>Overview</h2>
  <p>
    Understanding ${keyword} helps improve your digital marketing strategy and automation workflow.
  </p>

  <h2>Recommended Tool</h2>
  <p>
    Try this tool:
    <a href="${affiliate}" target="_blank" rel="noopener noreferrer">
      Access here
    </a>
  </p>

  <h2>Key Insights</h2>
  <ul>
    <li>${keyword} improves workflow efficiency</li>
    <li>Automation saves time and increases output</li>
    <li>Proper setup improves results</li>
  </ul>

  <h2>Conclusion</h2>
  <p>
    Using ${keyword} effectively can improve your overall marketing performance.
  </p>

</body>
</html>
`;
}

// ----------------------------
// SAVE PAGE
// ----------------------------
function savePage(keyword, html) {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const fileName = keyword
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

  const filePath = path.join(OUTPUT_DIR, `${fileName}.html`);

  fs.writeFileSync(filePath, html);
}

// ----------------------------
// MAIN GENERATOR (LIMIT RESPECTED)
// ----------------------------
function run() {

  const keywords = getKeywords();

  let created = 0;

  console.log(`🚀 Starting generation with limit: ${PAGE_LIMIT}`);

  for (let i = 0; i < keywords.length; i++) {

    // 🔥 HARD STOP (THIS ENFORCES YOUR LIMIT)
    if (created >= PAGE_LIMIT) {
      console.log(`🛑 Limit reached: ${PAGE_LIMIT} pages`);
      break;
    }

    const keyword = keywords[i];

    if (!isValidKeyword(keyword)) continue;

    const html = generateHTML(keyword);

    savePage(keyword, html);

    created++;
  }

  console.log(`✅ Completed: ${created} pages generated`);
}

// ----------------------------
// EXECUTE
// ----------------------------
run();
