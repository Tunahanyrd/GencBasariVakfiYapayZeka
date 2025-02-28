import requests
import datetime

API_KEY = "a56c0107aa874ca68d5b100a4268011d"  
BASE_URL = "https://newsapi.org/v2/"

def fetch_news(query="latest", from_date=None, to_date=None):
#haberleri getir
    url = BASE_URL + "everything"
    params = {
        "q": query,
        "apiKey": API_KEY,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("articles", [])
    else:
        print("haberler alınamadı:", response.status_code)
        return []

#crud yapacağımız liste
news_data_store = []

def create_news_item(item):
#haberi listeye atma
    news_data_store.append(item)
    print("haber oluşturuldu.")

def read_news_items():
#haberlerin döndürülmesi
    return news_data_store

def update_news_item(index, updated_item):
#belirtilen indextegi haberi güncelleme
    if 0 <= index < len(news_data_store):
        news_data_store[index] = updated_item
        print("haber güncellendi.")
    else:
        print("belirtilen index geçersiz.")

def delete_news_item(index):
#belirtilen haberi silme
    if 0 <= index < len(news_data_store):
        removed = news_data_store.pop(index)
        print("haber silindi.")
        return removed
    else:
        print("belirtilen index geçersiz.")
        return None

def search_news_by_period(period="daily", query="latest"):
#haberleri arama
    now = datetime.datetime.now()
    if period == "daily":
        from_date = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    elif period == "weekly":
        from_date = (now - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif period == "monthly":
        from_date = (now - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        print("Geçersiz zaman. 'daily', 'weekly' veya 'monthly' seçinicz.")
        return []

    to_date = now.strftime("%Y-%m-%d")
    articles = fetch_news(query=query, from_date=from_date, to_date=to_date)
    return articles

if __name__ == "__main__":
    #test amaçlı kullanım

    # 1. Günlük haberleri arama
    daily_news = search_news_by_period("daily", "technology")
    print(f"günlük {len(daily_news)} adet haber çekildi.")

    # 2. ilk haber öğesini yerel veri listesine ekleme (create)
    if daily_news:
        create_news_item(daily_news[0])

    # 3. Veri deposundaki haberleri okuma (read)
    items = read_news_items()
    print("mevcut haber öğeleri:")
    for idx, item in enumerate(items):
        print(f"{idx}: {item.get('title')}")

    # 4. İlk haberi güncelleme (update)
    if items:
        updated_item = items[0].copy()
        updated_item["title"] += " [Güncellendi]"
        update_news_item(0, updated_item)
        print("Güncellenmiş başlık:", read_news_items()[0].get("title"))

    # 5. İlk öğeyi silme (delete)
    delete_news_item(0)
    print("Son veri deposu içeriği:", read_news_items())
