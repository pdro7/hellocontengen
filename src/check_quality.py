# check_quality.py

import logging
from ai_client import generate_content
from content_validator import check_body_contains_keyword, check_title_length, is_fully_localized
from templates_loader import tpl

logger = logging.getLogger("pipeline")
MAX_CORRECTIONS = 3

def check_content_quality(content, locale, keyword):
    """
    Validates and fixes content quality issues.
    Returns the validated/fixed content or None if validation fails.
    """
    title_ok = False
    body_ok = False
    lang_ok = False

    # Title correction
    for attempt in range(1, MAX_CORRECTIONS + 1):
        
        if check_title_length(content["title"]):
            title_ok = True
            break
        
        corr_prompt = tpl.module.correction_title(
            bad_title=content['title'],
            length=len(content['title'])
        )

        logger.info(
            f"🔄 Title correction attempt {attempt}/{MAX_CORRECTIONS}",
            extra={"locale": locale, "keyword": keyword, "attempts": attempt}
        )

        correction = generate_content(corr_prompt)
        content['title'] = correction.get('title', content['title'])

    if title_ok:
        logger.info(
        "Title length is OK",
        extra={"extra_fields": {
            "locale": locale,
            "keyword": keyword,
            "length": len(content["title"]),
            "attempt": (f"{attempt}/{MAX_CORRECTIONS}")
            
        }}
    )
    else:
        logger.error(
            "Title still too long after corrections",
            extra={"locale": locale, "keyword": keyword, "attempts": MAX_CORRECTIONS}
        )
            
    

      
     #Correction keyword in body
    for attempt in range(1, MAX_CORRECTIONS + 1):
        if check_body_contains_keyword(content["body"], keyword):
            body_ok = True
            break
        corr_prompt = tpl.module.correct_kw_in_body(
            body=content['body'],
            keyword=keyword
        )
        logger.info(
            f"🔄 Body correction attempt {attempt}/{MAX_CORRECTIONS}",
            extra={"locale": locale, "keyword": keyword, "attempts": attempt}
        )
        correction = generate_content(corr_prompt)
        content['body'] = correction.get('body', content['body'])

    if body_ok:
        logger.info(
            "Keyword in body is OK",
            extra={"extra_fields": {
                "locale": locale,
                "keyword": keyword,
                "length": len(content["body"]),
                "attempt": (f"{attempt}/{MAX_CORRECTIONS}")
            }}
        )
    else:
        logger.error(
            "Body still missing keyword after corrections",
            extra={"locale": locale, "keyword": keyword, "attempts": MAX_CORRECTIONS}
        )
        
    #Language correction (single-language)
    
    for attempt in range(1, MAX_CORRECTIONS + 1):
        if is_fully_localized(content["body"], locale):
            lang_ok = True
            break
        corr_prompt = tpl.module.correction_language(
            text=content['body'],
            locale=locale
        )
        logger.info(
            f"🔄 Language correction attempt {attempt}/{MAX_CORRECTIONS}",
            extra={"locale": locale, "keyword": keyword, "attempts": attempt}
        )
        correction = generate_content(corr_prompt)
        content['body'] = correction.get('body', content['body'])

    if lang_ok:
        logger.info(
            "Content language OK",
            extra={"locale": locale, "keyword": keyword, "attempts": attempt}
        )
    else:
        logger.error(
            "Content still mixed-language after corrections",
            extra={"locale": locale, "keyword": keyword, "attempts": MAX_CORRECTIONS}
        )

    if title_ok and body_ok and lang_ok:
        return content


    logger.error(
        "Final validation failed",
        extra={
            "locale": locale,
            "keyword": keyword,
            "title_ok": title_ok,
            "body_ok": body_ok,
            "lang_ok": lang_ok
        }
    )
    return None
