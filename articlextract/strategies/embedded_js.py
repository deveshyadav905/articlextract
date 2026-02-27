from .base import BaseStrategy

class EmbeddedJSStrategy(BaseStrategy):
    ...
    
    
    
# def is_arc_article(global_content: dict) -> bool:
#     if not isinstance(global_content, dict):
#         return False

#     content = global_content.get("content_elements")
#     if not isinstance(content, list):
#         return False

#     has_text = any(
#         isinstance(el, dict) and el.get("type") == "text"
#         for el in content
#     )

#     has_headline = (
#         isinstance(global_content.get("headlines"), dict) and
#         isinstance(global_content["headlines"].get("basic"), str)
#     )

#     return has_text and has_headline

# # Example usage
# is_article = is_arc_article(fusion_metadata.get("globalContent", {}))
# print(is_article)