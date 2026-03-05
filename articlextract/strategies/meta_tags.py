import re
from .base import BaseStrategy
from ..cleaners.html_cleaner import clean_html


META_REGEX = re.compile(
    r'<meta\s+(?:name|property)=["\']([^"\']+)["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


class MetaTagStrategy(BaseStrategy):

    def extract(self) -> dict:

        meta_map = self._collect_meta()

        title = (
            meta_map.get("og:title")
            or meta_map.get("twitter:title")
            or self._extract_html_title()
        )

        description = (
            meta_map.get("og:description")
            or meta_map.get("description")
        )

        img_url = (
            meta_map.get("og:image")
            or meta_map.get("twitter:image")
        )

        author = (
            meta_map.get("author")
            or meta_map.get("article:author")
        )

        pubdate = (
            meta_map.get("article:published_time")
            or meta_map.get("pubdate")
            or meta_map.get("date")
        )

        modified_time = (
            meta_map.get("article:modified_time"),
            
        )
        link = (
            meta_map.get("og:url")
            or meta_map.get("twitter:url")
        )
        
        keywords = (
            meta_map.get("og:keywords")
            or meta_map.get("keywords")
            or meta_map.get("news_keywords")
        )

        language = (
            meta_map.get("og:locale")
        )
        
        source = (
            meta_map.get("og:site_name")
            or meta_map.get("twitter:site")
        )
                

        return {
            "link": link,
            "title": clean_html(title),
            "description": clean_html(description),
            "keywords" : keywords,
            "img_url": img_url,
            "author": author,
            "language": language,
            "pubdate": pubdate,
            "modified_time": modified_time,
            "source": source,
        }

    def _collect_meta(self) -> dict:
        """
        Extract meta tags into dictionary.
        """

        meta_map = {}

        matches = META_REGEX.findall(self.html)

        for key, value in matches:
            key = key.lower().strip()

            if key and value:
                meta_map[key] = value.strip()

        return meta_map

    def _extract_html_title(self):

        match = re.search(
            r"<title>(.*?)</title>",
            self.html,
            re.IGNORECASE | re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return None