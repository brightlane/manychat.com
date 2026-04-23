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
// 🧠 BLOG STRUCTURE (AI SECTIONS)
// =========================
const sections = [
  "What is ManyChat and how it works",
  "Why Instagram DM automation is powerful",
  "How businesses use ManyChat to generate leads",
  "Step-by-step setup guide for beginners",
  "Advanced funnel strategies for conversion",
  "Ecommerce automation with chatbots",
  "Creator monetization strategies using DM automation",
  "Common mistakes in automation marketing",
  "Scaling systems to 6-7 figures",
  "Future of AI marketing automation"
];

// =========================
// 🤖 OPENAI SECTION GENERATOR
// =========================
async function generateSection(topic) {

  const prompt = `
Write a detailed SEO blog section about:

"${topic}"

Requirements:
- 1500–2500 words
- deep explanation
- actionable insights
- business examples
- include modern marketing context
- natural tone (not robotic)
- include keyword variations naturally
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
// ✍️ HTML WRAPPER
// =========================
function wrapHTML(content) {
  return `
<!DOCTYPE html>
<html>
<head>
<title>Ultimate ManyChat Automation Guide</title>
<meta name="description" content="Deep guide to ManyChat automation and Instagram growth.">
</head>

<body style="font-family:Arial; max-width:900px; margin:40px; line-height:1.7;">

<h1>Ultimate ManyChat Automation Guide (25,000+ Words AI Edition)</h1>

<a href="${LINKS.free}">👉 Start Free Trial</a>

<hr>

${content}

<hr>

<h2>Start Now</h2>

<a href="${LINKS.ig}">👉 Instagram Automation</a><br>
<a href="${LINKS.pricing}">👉 Pricing</a><br>
<a href="${LINKS.main}">👉 Get Started</a>

</body>
</html>
`;
}

// =========================
// ⚙️ MAIN ENGINE
// =========================
async function run() {

  let fullContent = "";

  for (let i = 0; i < sections.length; i++) {

    console.log("Generating section:", sections[i]);

    const aiText = await generateSection(sections[i]);

    fullContent += `
<h2>${sections[i]}</h2>
<p>${aiText}</p>
`;
  }

  const html = wrapHTML(fullContent);

  fs.writeFileSync("blog.html", html);

  console.log("✅ AI 25K+ WORD BLOG GENERATED");
}

run();
