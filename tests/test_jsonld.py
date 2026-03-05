from articlextract.strategies.jsonld import JsonLDStrategy

HTML = """
<html>
<head>
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "NewsArticle",
 "headline": "JSONLD Title",
 "author": {
   "@type": "Person",
   "name": "Alice"
 },
 "datePublished": "2025-03-05",
 "image": "https://site.com/jsonld.jpg",
 "articleBody": "This is the full article text"
}
</script>
</head>
<body></body>
</html>
"""

def test_json_parser():
    
    strategy = JsonLDStrategy(HTML)
    
    data = strategy.extract()
    
    assert data["title"] == "JSONLD Title"
    assert data["author"] == "Alice"
    assert data["pubdate"] == "2025-03-05"
    assert data["img_url"] == "https://site.com/jsonld.jpg"
    assert "article text" in data["full_description"]