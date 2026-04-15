require("./generator-core").run();
// In vulture-generator.js - ENFORCE per page:
const pageQuality = {
  semanticH1: true,           // Unique H1 per page [cite:25]
  schemaJSONLD: true,         // FAQ/HowTo/Product [cite:24]
  wordCount: 800+,            // E-E-A-T depth
  internalLinks: 10+,         // Hub-spoke clusters [cite:21]
  mobileCSS: true,            // 100/100 Core Vitals
  uniqueMeta: true,           // Title/desc per keyword
  affiliateCTAs: 3,           // ManyChat links (non-spammy)
  readability: 70+            // Flesch score
};
