import pandas as pd 
import numpy as np 
from fastopic import FASTopic
from topmost import Preprocess
import streamlit as st

@st.cache_data
def train_and_infer(text:list[str] , n_words = 15 ): 
    clean_texts = [t for t in text if isinstance(t , str) and 8 < len(t.split()) < 120]
    if len(clean_texts) < 5 : 
        raise ValueError("samll text")
    n_docs = len(clean_texts)
    topics_nums = min(12, max(4, n_docs // 60))
    preprocess = Preprocess(vocab_size=8000)
    model = FASTopic(num_topics=topics_nums , preprocess=preprocess , verbose=False , normalize_embeddings=True  )
    _ , topics = model.fit_transform(clean_texts)
    topics = np.argmax(topics , axis=1)
    keywords = {}
    for topic_id in set(topics): 
        words_probs = model.get_topic(topic_id)
        keywords[topic_id] = [word for word , _ in words_probs if len(word) > 3][:n_words]
    results_df = pd.DataFrame({
        "text": clean_texts,
        "topic": topics
    })
    
    return results_df, keywords