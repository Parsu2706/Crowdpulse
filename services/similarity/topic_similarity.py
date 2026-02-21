from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


@st.cache_resource
def get_embed_model(): 
    return SentenceTransformer('all-MiniLM-L6-v2')

model = get_embed_model()

@st.cache_data
def semantic_topic_similarity(words_a : list[str] , words_b : list[str]) -> float: 
    text_a = "This topic discusses " + ", ".join(words_a)
    text_b = "This topic discusses " + ", ".join(words_b)

    embed =  model.encode([text_a , text_b] , normalize_embeddings=True)
    score = float(cosine_similarity([embed[0]] , [embed[1]])[0][0])
    return round(score , 3)


