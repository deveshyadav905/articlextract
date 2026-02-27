from .base import BaseStrategy
from ..parsers.jsonld_parser import parse_jsonld
from ..cleaners.html_cleaner import clean_html


class JsonLDStrategy(BaseStrategy):

    ARTICLE_TYPES = {
        "article",
        "newsarticle",
        "blogposting",
        "reportagenewsarticle",
        "backgroundnewsarticle",
        "opinionnewsarticle",
    }

    def extract(self) -> dict:

        result = {}

        items = parse_jsonld(self.html)

        for item in items:

            types = self._get_types(item)

            if not any(t in self.ARTICLE_TYPES for t in types):
                continue

            # TITLE
            title = item.get("headline")

            # BODY
            body = self._extract_body(item)

            # IMAGE
            img = self._extract_image(item)

            # AUTHOR
            author = self._extract_author(item)

            # PUBDATE
            pubdate = (
                item.get("datePublished")
                or item.get("dateCreated")
            )

            # LINK
            link = self._extract_link(item)

            # SOURCE
            source = self._extract_source(item)

            result.update({
                "title": title,
                "full_description": body,
                "img_url": img,
                "author": author,
                "pubdate": pubdate,
                "link": link,
                "source": source,
            })

            break  # first valid article wins

        return result

    def _get_types(self, item):
        atype = item.get("@type")

        if isinstance(atype, str):
            return [atype.lower()]

        if isinstance(atype, list):
            return [t.lower() for t in atype if isinstance(t, str)]

        return []

    def _extract_body(self, item):
        body = item.get("articleBody")

        if isinstance(body, list):
            body = " ".join(body)

        return clean_html(body)

    def _extract_image(self, item):
        image = item.get("image")

        if isinstance(image, str):
            return image

        if isinstance(image, dict):
            return image.get("url") or image.get("@id")

        if isinstance(image, list):
            for img in image:
                if isinstance(img, str):
                    return img
                if isinstance(img, dict):
                    return img.get("url")

        return None

    def _extract_author(self, item):
        author = item.get("author")

        if isinstance(author, str):
            return author

        if isinstance(author, dict):
            return author.get("name")

        if isinstance(author, list):
            names = []
            for a in author:
                if isinstance(a, dict):
                    name = a.get("name")
                    if name:
                        names.append(name)
            return ", ".join(names) if names else None

        return None

    def _extract_link(self, item):
        mep = item.get("mainEntityOfPage")

        if isinstance(mep, str):
            return mep

        if isinstance(mep, dict):
            return mep.get("@id") or mep.get("url")

        return item.get("url")

    def _extract_source(self, item):
        publisher = item.get("publisher")

        if isinstance(publisher, dict):
            return publisher.get("name")

        return None