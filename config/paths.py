from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
REDDIT_CSV = DATA_RAW / "reddit_latest.csv"
NEWS_CSV = DATA_RAW / "news_latest.csv"




import asyncio

LLM_SEMAPHORE = asyncio.Semaphore(2)  
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_topic_similarity(words_a : list[str] , words_b : list[str]) -> float: 
    text_a  = " ".join(words_a)
    text_b  = " ".join(words_b)

    embeddigs = model.encode([text_a , text_b] , normalize_embeddings =True)
    score = cosine_similarity(
        embeddigs[0].reshape(1, -1),
        embeddigs[1].reshape(1, -1),
    )[0][0]

    return float(score)