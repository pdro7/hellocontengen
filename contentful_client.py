# contentful_client.py
import os
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import json



# Loading Contentful credentials
SPACE = os.getenv('CONTENTFUL_SPACE_ID')
ENV = os.getenv('CONTENTFUL_ENVIRONMENT')
TOKEN = os.getenv('CONTENTFUL_ACCESS_TOKEN')
CONTENT_TYPE_ID = "productDescription" 

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def create_draft_entry(locale, keyword, product, content):
    if locale == "nl-NL": locale = "nl"

    url = f"https://api.contentful.com/spaces/{SPACE}/environments/{ENV}/entries"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/vnd.contentful.management.v1+json",
        "X-Contentful-Content-Type": "helloProduct"
    }
    
    # Build the payload according to Sample Draft Entries
    payload = {
      
      "fields": {
        "title": { locale: content["title"] },
        "slug":  { locale: keyword.replace(" ", "-").lower() },
        "body":  { locale: content["body"] },
        #"metaDescription": { locale: content["meta"] },
        "keywords": { locale: [keyword] },
        "category": { locale: product["category"] }
      }
    }
    
    print(payload) # DEBUG
  
    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Show the response status
    if response.status_code == 201:
        print("✅ Draft sucessfully created")
        print("Entry ID:", response.json().get("sys", {}).get("id"))
    else:
        print("❌ Error al crear el draft")
        print("Status:", response.status_code)
        print("Mensaje:", response.text)

    return response.json()