# run_pipeline.py
import random
from check_quality import check_content_quality
from pipeline import load_keywords, load_products, select_keywords
from ai_client import generate_content
from contentful_client import create_draft_entry
from templates_loader import tpl
import logging

from logging_setup import JsonFormatter
from dotenv import load_dotenv
load_dotenv()

# JSON logger configuration
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# File handler for JSON logging
file_h = logging.FileHandler("logs/pipeline.json", encoding="utf-8")
file_h.setFormatter(JsonFormatter())
logger.addHandler(file_h)

def main():
    keywords = load_keywords()
    products = load_products()
    locales = ["en-US", "nl-NL"] 
    sel = select_keywords(keywords, locales, n=1)
    print("Keywords selection by locale:", sel)

    # Choose a single example product
    product_example = products[random.randint(1, len(products)-1)]
    

    for locale, kw_list in sel.items():
        for keyword in kw_list:
            
            # Generate the prompt using the template
            prompt = tpl.module.generation_prompt(
                locale=locale,
                keyword=keyword,
                product_name=product_example["product_name"],
                price=f"${product_example['base_price_usd']}",
                features=f"Lead time: {product_example['lead_time_days']} days"                
            )

            

            try:
                content = generate_content(prompt)

                content = check_content_quality(content, locale, keyword)
                
                response = create_draft_entry(locale, keyword, product_example, content)
                logger.info("Draft sucessfully created", extra={"locale": locale, "keyword": keyword, "response": response.status_code})

                
                
            except Exception as e:
                logger.info("Draft sucessfully created", extra={"locale": locale, "keyword": keyword, "response": response.status_code})
                

if __name__ == "__main__":
    main()
