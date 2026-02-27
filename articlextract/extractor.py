from .strategies.jsonld import JsonLDStrategy
from .strategies.embedded_js import EmbeddedJSStrategy
from .strategies.meta_tags import MetaTagStrategy


class ContentExtractor:

    def __init__(self, html: str, url: str | None = None):
        self.html = html
        self.url = url

        self.strategies = [
            JsonLDStrategy(html, url),
            EmbeddedJSStrategy(html, url),
            MetaTagStrategy(html, url),
        ]

    def extract(self) -> dict:
        result = {
            "title": None,
            "link": self.url,
            "full_description": None,
            "img_url": None,
            "author": None,
            "pubdate": None,
            "source": None,
        }

        for strategy in self.strategies:
            try:
                data = strategy.extract()
                if not data:
                    continue
            except Exception as e:
                print(str(e))

            for key, value in data.items():
                if result.get(key) is None and value:
                    result[key] = value

        return result