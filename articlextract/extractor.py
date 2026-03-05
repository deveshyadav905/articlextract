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
            "link": self.url,
            "title": None,
            "description": None,
            "keywords": None,
            "img_url": None,
            "author": None,
            "language": None,
            "pubdate": None,
            "modified_time": None,
            "source": None,
            "full_description": None
        }

        for strategy in self.strategies:
            try:
                data = strategy.extract()
                if not data:
                    continue
            except Exception as e:
                continue

            for key, value in data.items():
                if result.get(key) is None and value:
                    result[key] = value
            
            if not any(value != None for key,value in result.items()):
                break

        return result