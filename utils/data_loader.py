import pandas as pd
from config.paths import REDDIT_CSV , NEWS_CSV

def get_file_mtime(news:bool = False):
    if news: 
        return NEWS_CSV.stat().st_mtime if NEWS_CSV.exists() else None
    
    return REDDIT_CSV.stat().st_mtime if REDDIT_CSV.exists() else None



def load_latest_data(news:bool = False) -> pd.DataFrame:
    if news: 
        if not NEWS_CSV.exists(): 
            return pd.DataFrame()
        return pd.read_csv(NEWS_CSV)

    if not REDDIT_CSV.exists():
        return pd.DataFrame()
    return pd.read_csv(REDDIT_CSV)

