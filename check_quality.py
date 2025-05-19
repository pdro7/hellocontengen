# check_quality.py

import logging
from ai_client import generate_content
from content_validator import check_body_contains_keyword, check_title_length, is_fully_localized
from templates import tpl

logger = logging.getLogger("pipeline")

def check_content_quality(content, locale, keyword):
    """
    Validates and fixes content quality issues.
    Returns the validated/fixed content or None if validation fails.
    """
    # Check title length
    if not check_title_length(content["title"]):
        print(f"❌ [{locale}|{keyword}] Title too long ({len(content['title'])} chars)")

        #correction = generate_content(f""" The title "{content['title']}" is too long ({len(content['title'])} chars).
         #               Please return **only** a new JSON object with a `title` field ≤ 60 chars.""")

        correction = generate_content(tpl.module.correction_title(content['title'], len(content['title'])))
        
        new_title = correction["title"]
        
        if check_title_length(new_title):
            content["title"] = new_title
        else:
            content["title"] = new_title[:60].rstrip()
            logger.warning("Título truncado tras re-prompt", 
                            extra={"locale": locale, "keyword": keyword})
    else:
        logger.info(
            "Title length OK",
            extra={"extra_fields": {
                "locale": locale,
                "keyword": keyword,
                "length": len(content["title"])
            }}
        )

    # Check keyword in body
    if not check_body_contains_keyword(content["body"], keyword):
        #correction = generate_content(f"""The body you generated does not include the keyword "{keyword}".
         #                               Please return **only** a JSON object with a new `body` field that **must** include that keyword.""")
        correction = generate_content(tpl.module.correct_kw_in_body(content["body"], keyword))

        content["body"] = correction["body"]
    else:
        logger.info(
            "Keyword in body OK",
            extra={"extra_fields": {
                "locale": locale,
                "keyword": keyword,
                "length": len(content["body"])
            }}
        )

    # Check language
    if not is_fully_localized(content["body"], locale):
        logger.warning("Mixed-language content detected", 
                        extra={"locale": locale, "keyword": keyword})
        return None

    return content