from .base import BaseStrategy
from ..parsers.jsonld_parser import parse_jsonld,flatten_itmes
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
            
            #DESCRIPTION
            description = item.get("description")
            
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

            modified_time = (
                item.get("dateModified")
            )
            
            # KEYWORDS
            keywords =  item.get("keywords")
            
            # LANGUAGE
            language = item.get("inLanguage")

            # LINK
            link = self._extract_link(item)
            
            source_info = self._extract_source_info(item)
            
            source = source_info.get("name")
            
            logo = source_info.get('logo')
            
            result.update({
                
                "link": link,
                "title": title,
                "description": description,
                "keywords": keywords,
                "language": language,
                "img_url": img,
                "full_description": body,
                "author": author,
                "pubdate": pubdate,
                "modified_time": modified_time,
                "source": source,
                "logo": logo
    
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
    
    def _extract_source_info(self, item):
        source_info = {}

        publisher = item.get("publisher")
        if publisher:
            source_info["name"] = publisher.get("name")
            source_info["logo"] = publisher.get('logo').get('url') if isinstance(publisher.get('logo'),dict) else None
                
        return source_info