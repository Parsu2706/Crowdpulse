import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from config.paths import NEWS_CSV, DATA_RAW
from config.news_queries import NEWS_QUERIES
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://newsdata.io/api/1/latest")
NEWS_QUERIES = NEWS_QUERIES

max_article_per_topic = 40 
requests_timeout = 10 

def fetch_news_article()->pd.DataFrame: 
    if not API_KEY : 
        raise ValueError("Get a valid API key")
    all_articles = []
    
    print(f"Fetching live news")
    for topic , query in NEWS_QUERIES.items(): 
        next_page = None
        collected = []
        print(f"Fetching topic: {topic}")
        page_count = 0
        while len(collected) < max_article_per_topic and page_count < 10:

            params = {
                "apikey" : API_KEY , 
                "q" : query , 
                "language" : "en"
            }
            if next_page : 
                params["page"] = next_page
            try: 
                response = requests.get(BASE_URL , params= params , timeout=requests_timeout)

                response.raise_for_status()
                data = response.json()
                page_count += 1

            except requests.RequestException as e : 
                print("Failed to fetch : " ,topic ,e)
                break
            results = data.get("results", [])            
            if not results: 
                break
            collected.extend(results)
            next_page = data.get("nextPage")
            if not next_page: 
                break

        collected = collected[:max_article_per_topic]
        for article in collected:           
            text = " ".join(filter(None, [
                article.get("title"),
                article.get("description"),
                article.get("content")
            ]))
 
            all_articles.append({
                "topic": topic,
                "title": article.get("title"),
                "text": text,
                "url": article.get("link"),
                "published": article.get("pubDate"),
                "publisher": article.get("source_id"),
                "source": "news",
                "fetched_at": datetime.utcnow().isoformat()
            })
        print(f"{topic}: {len(collected)} articles")
    df = pd.DataFrame(all_articles)
    df = (df.drop_duplicates(subset="title").dropna(subset=["text"]).reset_index(drop=True))
    df = df[df["text"].str.split().str.len() > 20]
    df = df.reset_index(drop=True)

    print(f"\nTotal articles fetched: {len(df)}\n")
    DATA_RAW.mkdir(parents=True , exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    version_path = DATA_RAW/f"news_{timestamp}.csv"
    df.to_csv(version_path , index=False)
    df.to_csv(NEWS_CSV , index=False)
    print("Loaded API KEY:", repr(API_KEY))

    return df