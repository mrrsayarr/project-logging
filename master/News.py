"""
https://newsapi.org/
2019020@ogrenci.amasya.edu.tr maili ile çekildi
"""

import requests
from datetime import datetime, timedelta

"""
6e62fe2735f94fc5b75577dab9853d73
"""
api_key = "----------------" # News API

def get_cybersecurity_news(from_date=None, to_date=None, sources=None):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "cybersecurity",
        "apiKey": api_key,
        "sortBy": "publishedAt"
    }
    if from_date:
        params["from"] = from_date.strftime("%Y-%m-%d")
    if to_date:
        params["to"] = to_date.strftime("%Y-%m-%d")
    if sources:
        params["sources"] = ",".join(sources)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        for article in articles:
            print(f"Kaynak: {article['source']['name']}")
            print(f"Başlık: {article['title']}")
            print(f"Tarih: {article['publishedAt']}")
            print(f"URL: {article['url']}")
            print("-" * 50)
    else:
        print(f"Hata: {response.status_code}")

if __name__ == "__main__":
    # Son 7 günün haberlerini al
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    get_cybersecurity_news(from_date=week_ago, to_date=today)

    # Belirli kaynaklardan haberleri al (örnek)
    # sources = ["the-verge", "wired"]
    # get_cybersecurity_news(sources=sources)