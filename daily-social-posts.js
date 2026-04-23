import fs from "fs";

// =========================
// 🔗 AFFILIATE LINK
// =========================
const CTA = "https://manychat.partnerlinks.io/bbwxetk27f88-64kfxo";

// =========================
// 📁 LOAD DAILY ARTICLE
// =========================
function loadLatestArticle() {

  const folder = "./daily";

  if (!fs.existsSync(folder)) {
    console.log("No daily folder found");
    return null;
  }

  const files = fs.readdirSync(folder).filter(f => f.endsWith(".html"));

  if (files.length === 0) return null;

  const latest = files.sort().pop();

  const content = fs.readFileSync(`${folder}/${latest}`, "utf-8");

  return {
    file: latest,
    content
  };
}

// =========================
// 🧠 EXTRACT TITLE (simple parser)
// =========================
function extractTitle(html) {
  const match = html.match(/<h1>(.*?)<\/h1>/);
  return match ? match[1] : "Automation Marketing Guide";
}

// =========================
// ✍️ SOCIAL POST GENERATOR
// =========================
function createPosts(title) {

  const hooks = [
    `🚀 Most people are sleeping on ${title}`,
    `🔥 This is how you fix ${title}`,
    `💡 ${title} explained simply`,
    `📈 Why ${title} matters right now`
  ];

  const hook = hooks[Math.floor(Math.random() * hooks.length)];

  const base = `
${hook}

Businesses are using automation to scale faster than ever.

Instead of doing everything manually, tools like ManyChat automate the entire process.

👉 Start here: ${CTA}

#marketing #automation #business #growth
`;

  return {
    x: base,
    instagram: base,
    facebook: base
  };
}

// =========================
// 📤 OPTIONAL BUFFER FORMAT (REAL SCHEDULER)
// =========================
function bufferFormat(post, url) {
  return {
    text: post,
    media: { link: url }
  };
}

// =========================
// ⚙️ MAIN ENGINE
// =========================
function run() {

  const article = loadLatestArticle();

  if (!article) {
    console.log("No article found");
    return;
  }

  const title = extractTitle(article.content);

  console.log("Creating social posts for:", title);

  const posts = createPosts(title);

  const output = {
    title,
    file: article.file,
    posts: posts
  };

  if (!fs.existsSync("social")) {
    fs.mkdirSync("social");
  }

  fs.writeFileSync(
    `social/${article.file}-posts.json`,
    JSON.stringify(output, null, 2)
  );

  console.log("✅ Social posts generated");

  console.log("\nX POST:\n", posts.x);
  console.log("\nINSTAGRAM POST:\n", posts.instagram);
  console.log("\nFACEBOOK POST:\n", posts.facebook);
}

run();
