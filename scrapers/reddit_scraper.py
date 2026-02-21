import praw 
import pandas as pd 
import datetime 
import os 
import prawcore
import logging
from dotenv import load_dotenv
from pathlib import Path 
from config.paths import DATA_RAW, REDDIT_CSV

DATA_RAW.mkdir(parents=True, exist_ok=True)


load_dotenv()

LIMIT = 100
raw_data_dir  = "data/raw"
out_file = "reddit_latest.csv"
os.makedirs(raw_data_dir, exist_ok=True)
logging.basicConfig(level=logging.INFO)

def load_subreddits(path: str = "config/subreddits.txt") -> list[str]: 
    if not os.path.exists(path): 
        raise FileNotFoundError(f"subreddits.txt not found")
    with open(path , 'r' , encoding='utf-8') as f: 
        return [line.strip() for line in f if line.strip()]

def init_reddit():
    return praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
)

def scrape_subreddit(reddit, subreddit_name):
    posts = []
    try:
        logging.info(f"scrapping subreddit : {subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)
    
        for post in subreddit.hot(limit=LIMIT):
            if post.stickied:
                continue
            posts.append({
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'num_comments': post.num_comments,
                'upvote_ratio': post.upvote_ratio,
                'created_utc': datetime.datetime.utcfromtimestamp(post.created_utc).isoformat(),
                'subreddit': subreddit_name,
                'url': post.url
            })
        return posts

    except prawcore.exceptions.Forbidden:
        logging.warning(f"Subreddit {subreddit_name} is private")
        return []
    except prawcore.exceptions.NotFound:
        logging.warning(f"Subreddit {subreddit_name} not found")
        return []
    except Exception as e:
        logging.error(f"Error occurred during scraping {subreddit_name}: {e}", exc_info=True)
        return []
    return posts
    

def run_scrapper() -> Path:

    reddit = init_reddit()
    subreddits = load_subreddits()
    all_posts : list[dict] = []
    for sub in subreddits: 
        all_posts.extend(scrape_subreddit(reddit , sub))
    if not all_posts: 
        logging.warning("No posts scraped")
        return REDDIT_CSV
    df = pd.DataFrame(all_posts)
    df['source'] = 'reddit'
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    version_path = DATA_RAW / f"reddit_{timestamp}.csv"
    df.to_csv(version_path , index=False)
    df.to_csv(REDDIT_CSV, index=False)
    logging.info(f"Saved {len(df)} posts")
    logging.info(f"Versioned dataset: {version_path.name}")
    logging.info(f"Latest dataset: {REDDIT_CSV.name}")

    return version_path

if __name__ == '__main__':
    run_scrapper()