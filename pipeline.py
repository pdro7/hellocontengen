# pipeline.py
import csv
import random


def load_keywords(path="keywords.csv"):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def load_products(path="products.csv"):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def select_keywords(keywords, locales, n=3):
    by_locale = {}
    for loc in locales:
        filt = [k["keyword"] for k in keywords if k["locale"] == loc]
        by_locale[loc] = random.sample(filt, min(n, len(filt)))
    return by_locale

if __name__ == "__main__":
    keywords = load_keywords()
    products = load_products()
    locales = ["en-US", "nl-NL"] 
    sel = select_keywords(keywords, locales, n=3)
    print(sel)
