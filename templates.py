# templates.py
from jinja2 import Template

PROMPT_TMPL = Template("""
Locale: {{ locale }}
Keyword: {{ keyword }}
Product Name: {{ product_name }}
Price: {{ price }}
Features: {{ features }}
                       
You are a seach optimization engine experte and multilingual marketing copywriter.
                       
 
Produce all output exclusively in the language indicate by {{ locale }} , with absolutely no content in any other language.
                       
1) Write a **Title** (<= 60 characters). 
2) Write a **body** of ~150 words, it should include the keyword.
3) Write a **Meta description** (<= 155 characters).

You must respond only with a valid JSON object (no markdown, no extra fields, no code fences), using this structure:                       

{
  "title": "...",
  "body": "...",
  "meta": "..."
}

Do not add explanations, extra line breaks, comments, or any characters outside the JSON object.

Ensure the response is a valid JSON object, ready to parse.
                       

""".strip())
