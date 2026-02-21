import os
import pickle
import faiss
import numpy as np
import streamlit as st
from services.similarity.topic_similarity import get_embed_model


direct = "data/vector_storage"

@st.cache_resource
def get_model(): 
    return get_embed_model()


def create_path_check(name): 
    folder = os.path.join(direct , name)
    os.makedirs(folder , exist_ok=True)
    return (os.path.join(folder , "index..faise") , os.path.join(folder , "chunks.pkl"))
