// ===============================
// MANYCHAT AFFILIATE ENGINE v1.0
// ===============================

// === YOUR AFFILIATE LINKS ===
const AFF = {
  default: "https://manychat.partnerlinks.io/nwkkk7vkps17",
  free: "https://manychat.partnerlinks.io/emwcbue22i01-ogcg6e",
  discount: "https://manychat.partnerlinks.io/t8let4hhqtqg-wki14",
  pricing: "https://manychat.partnerlinks.io/98hj6b3pr28k-4znb59",
  instagram: "https://manychat.partnerlinks.io/8k59yhm0l32j-z7dk2i"
};

// === SIMPLE ROTATION (A/B TEST) ===
function getPrimaryOffer() {
  const options = [AFF.free, AFF.discount];
  return options[Math.floor(Math.random() * options.length)];
}

// === CLICK TRACKING ===
function trackClick(type) {
  const data = JSON.parse(localStorage.getItem("mc_clicks") || "{}");
  data[type] = (data[type] || 0) + 1;
  localStorage.setItem("mc_clicks", JSON.stringify(data));
}

// === SAFE LINK REPLACEMENT ===
document.querySelectorAll("a").forEach(link => {
  try {
    const url = new URL(link.href);

    // Only replace NON-affiliate ManyChat links
    if (
      url.hostname.includes("manychat.com") &&
      !url.hostname.includes("partnerlinks.io")
    ) {
      link.href = AFF.default;
    }

    // Track clicks
    link.addEventListener("click", () => trackClick(link.href));

  } catch (e) {}
});

// === CTA BUTTON GENERATOR ===
function createCTA(text, url) {
  const btn = document.createElement("a");
  btn.href = url;
  btn.innerText = text;

  btn.style.display = "block";
  btn.style.background = "#ff5a00";
  btn.style.color = "#fff";
  btn.style.padding = "14px";
  btn.style.margin = "25px 0";
  btn.style.textAlign = "center";
  btn.style.borderRadius = "8px";
  btn.style.fontWeight = "bold";
  btn.style.fontSize = "16px";
  btn.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";

  btn.addEventListener("click", () => trackClick(text));

  return btn;
}

// === SMART CTA INSERTION ===
function injectCTAs() {
  const sections = document.querySelectorAll("h2");
  const primaryOffer = getPrimaryOffer();

  sections.forEach((section, index) => {
    if (index === 1) {
      section.after(createCTA("🔥 Get 1 Month FREE of ManyChat", AFF.free));
    }

    if (index === 3) {
      section.after(createCTA("🚀 Automate Instagram DMs Now", AFF.instagram));
    }

    if (index === 5) {
      section.after(createCTA("💸 Get 50% Off ManyChat Pro", AFF.discount));
    }

    // Light rotation CTA
    if (index % 4 === 0) {
      section.after(createCTA("👉 Start Free ManyChat Account", primaryOffer));
    }
  });
}

// === EXIT INTENT POPUP ===
function createExitPopup() {
  const popup = document.createElement("div");
  popup.innerHTML = `
    <div style="
      position:fixed;
      top:0;left:0;width:100%;height:100%;
      background:rgba(0,0,0,0.7);
      display:flex;
      align-items:center;
      justify-content:center;
      z-index:9999;">
      
      <div style="
        background:#fff;
        padding:30px;
        max-width:400px;
        text-align:center;
        border-radius:10px;">
        
        <h2>Wait! Don’t Miss This</h2>
        <p>Get 1 Month FREE of ManyChat Pro before you go.</p>
        
        <a href="${AFF.free}" style="
          display:block;
          background:#ff5a00;
          color:#fff;
          padding:12px;
          margin-top:15px;
          text-decoration:none;
          border-radius:6px;
          font-weight:bold;">
          Claim Free Month
        </a>

        <p style="margin-top:10px;cursor:pointer;" id="closePopup">No thanks</p>
      </div>
    </div>
  `;

  document.body.appendChild(popup);

  document.getElementById("closePopup").onclick = () => popup.remove();
}

// Trigger exit intent
let exitShown = false;
document.addEventListener("mouseout", function(e) {
  if (!exitShown && e.clientY < 10) {
    exitShown = true;
    createExitPopup();
  }
});

// === INIT ===
document.addEventListener("DOMContentLoaded", () => {
  injectCTAs();
});

// === DEBUG (optional: check in console) ===
window.showMCStats = function() {
  console.log("ManyChat Click Stats:", JSON.parse(localStorage.getItem("mc_clicks") || "{}"));
};
