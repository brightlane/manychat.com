export function buildMeta({ title, description, url, keywords = "" }) {

  return `
<!-- SEO META TAGS -->
<title>${title}</title>
<meta name="description" content="${description}">
<meta name="keywords" content="${keywords}">

<!-- Indexing -->
<meta name="robots" content="index, follow">
<link rel="canonical" href="${url}">

<!-- Open Graph (Facebook, LinkedIn, Discord) -->
<meta property="og:type" content="article">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${description}">
<meta property="og:url" content="${url}">
<meta property="og:site_name" content="Automation Blog">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${title}">
<meta name="twitter:description" content="${description}">

<!-- SEO Extras -->
<meta name="author" content="Automation System">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Structured Data (Google SEO BOOST) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${title}",
  "description": "${description}",
  "url": "${url}"
}
</script>
`;
}
