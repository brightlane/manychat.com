import fs from "fs";
import fetch from "node-fetch";

// =========================
// 🔑 OPENAI KEY
// =========================
const OPENAI_API_KEY = "PUT_YOUR_KEY_HERE";

// =========================
// 🔗 AFFILIATE LINKS
// =========================
const LINKS = {
  main: "https://manychat.partnerlinks.io/nwkkk7vkps17",
  ig: "https://manychat.partnerlinks.io/bbwxetk27f88-64kfxo",
  free: "https://manychat.partnerlinks.io/emwcbue22i01-ogcg6e",
  insta: "https://manychat.partnerlinks.io/8k59yhm0l32j-z7dk2i",
  pricing: "https://manychat.partnerlinks.io/98hj6b3pr28k-4znb59"
};

// =========================
// 🧠 DAILY TOPIC POOL
// (expand this to 1000+ later)
// =========================
const topics = [
  "Instagram DM automation strategies",
  "How creators make money with automation",
  "Ecommerce chatbot funnels",
  "Lead generation with Instagram",
  "WhatsApp marketing automation",
  "How to increase Instagram conversions",
  "DM marketing psychology",
  "AI automation for small business growth",
  "Sales funnels using chatbots",
  "Future of marketing automation"
];

// =========================
// 📅 GET TODAY DATE
// =========================
function getDate() {
  const d = new Date();
  return d.toISOString().split("T")[0];
}

// =========================
// 🤖 GENERATE ARTICLE
// =========================
async function generateArticle(topic) {

  const prompt = `
Write a high-quality SEO blog article about:

"${topic}"

Requirements:
- 2000–3000 words
- detailed explanations
- examples and strategies
- marketing focus
- include natural keyword variation
- include automation mindset
`;

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are an expert SEO marketing writer." },
        { role: "user", content: prompt }
      ]
    })
  });

  const data = await res.json();
  return data.choices[0].message.content;
}

// =========================
// 🌐 HTML WRAPPER
// =========================
function wrapHTML(title, content) {

  return `
<!DOCTYPE html>
<html>
<head>
<title>${title}</title>
<meta name="description" content="${title} guide using automation.">
</head>

<body style="font-family:Arial; max-width:900px; margin:40px; line-height:1.7;">

<h1>${title}</h1>

<a href="${LINKS.free}">👉 Start Free Trial</a>

<hr>

${content}

<hr>

<h2>Start Automating</h2>

<a href="${LINKS.ig}">👉 Instagram Automation</a><br>
<a href="${LINKS.pricing}">👉 Pricing</a><br>
<a href="${LINKS.main}">👉 Get Started</a>

</body>
</html>
`;
}

// =========================
// ⚙️ MAIN DAILY ENGINE
// =========================
async function run() {

  const date = getDate();

  // pick topic based on day rotation
  const topic = topics[Math.floor(Math.random() * topics.length)];

  console.log("Generating daily article:", topic);

  const article = await generateArticle(topic);

  const html = wrapHTML(topic, article);

  if (!fs.existsSync("daily")) {
    fs.mkdirSync("daily");
  }

  const fileName = `daily-${date}.html`;

  fs.writeFileSync(`daily/${fileName}`, html);

  console.log("✅ DAILY ARTICLE CREATED:", fileName);
}

run();
