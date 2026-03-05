from articlextract.strategies.meta_tags import MetaTagStrategy


HTML = """
<html>
<head>
<meta property="og:title" content="Breaking News">
<meta property="og:description" content="World news today">
<meta property="og:image" content="https://site.com/img.jpg">
<meta property="article:author" content="John Doe">
<meta property="article:published_time" content="2025-03-05">
<meta property="og:url" content="https://site.com/article">
<meta property="og:site_name" content="Example News">
<title>Fallback Title</title>
</head>
<body></body>
</html>
"""


def test_meta_extraction():

    strategy = MetaTagStrategy(HTML)

    data = strategy.extract()

    assert data["title"] == "Breaking News"
    assert data["img_url"] == "https://site.com/img.jpg"
    assert data["author"] == "John Doe"
    assert data["pubdate"] == "2025-03-05"
    assert data["link"] == "https://site.com/article"
    assert data["source"] == "Example News"