import re
import json

JSONLD_REGEX = re.compile( r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

def extract_jsonld_bloks(html: str) -> list:
    """
    Extract raw JSON-LD script contents.
    """
    if not html:
        return []
    
    return JSONLD_REGEX.findall(html)

def parse_jsonld(html:str) -> list[dict]:
    """
    Parse and normalize all JSON-LD bloks.
    Return list of dict items
    """
    items = []
    
    blocks = extract_jsonld_bloks(html)
    
    for block in blocks:
        try:
            data = json.loads(block)
        except Exception as e:
            continue
        
        flat_items = flatten_itmes(data)    
        if flat_items:
            items.extend(flat_items)
        
    return items
        
def flatten_itmes(data) -> list[dict]:
    """
    Flat multilevel-dict @graph to list[dict]
    """
    if isinstance(data,dict):
        if '@graph' in data:
            return flatten_itmes(data['@graph'])
        return [data]
    
    if isinstance(data,list):
        return [item for item in data if isinstance(item,dict)]
            
    return []