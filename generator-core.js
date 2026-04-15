const fs = require("fs");
const path = require("path");

const OUTPUT_DIR = path.join(__dirname, "pages");

// 🔥 LIMIT CONTROLLED FROM GITHUB ACTIONS
const LIMIT = parseInt(process.env.PAGE_LIMIT_PER_RUN || "20");

// AFFILIATES
const AFFILIATES = [
  process.env.AFFILIATE_1,
  process.env.AFFILIATE_2,
  process.env.AFFILIATE_3,
  process.env.AFFILIATE_4,
  process.env.AFFILIATE_5
].filter(Boolean);

// --------------------
// KEYWORDS
// --------------------
function getKeywords() {
  return [
    "instagram automation tools",
    "manychat chatbot guide",
    "ai marketing tools",
    "lead generation strategies",
    "social media automation"
  ];
}

// --------------------
// AFFILIATE ROTATION
// --------------------
let idx = 0;
function getAffiliate() {
  if (AFFILIATES.length === 0) return "#";
  return AFFILIATES[idx++ % AFFILIATES.length];
}

// --------------------
// HTML BUILDER
// --------------------
function buildPage(keyword) {
  return `
<!DOCTYPE html>
<html>
<head>
  <title>${keyword}</title>
  <meta name="description" content="${keyword}">
</head>
<body>

  <h1>${keyword}</h1>

  <p>Guide about ${keyword}</p>

  <a href="${getAffiliate()}">Try Tool</a>

</body>
</html>
`;
}

// --------------------
// SAVE
// --------------------
function save(keyword, html) {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR);
  }

  const file = keyword.toLowerCase().replace(/[^a-z0-9]+/g, "-");

  fs.writeFileSync(
    path.join(OUTPUT_DIR, file + ".html"),
    html
  );
}

// --------------------
// RUNNER (LIMIT RESPECTED)
// --------------------
function run() {

  const keywords = getKeywords();
  let created = 0;

  for (let i = 0; i < keywords.length; i++) {

    if (created >= LIMIT) break;

    const keyword = keywords[i];
    const html = buildPage(keyword);

    save(keyword, html);

    created++;
  }

  console.log(`✅ Generated ${created} pages (limit ${LIMIT})`);
}

module.exports = { run };
