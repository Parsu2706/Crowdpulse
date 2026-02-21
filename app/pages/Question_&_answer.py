import streamlit as st
import pandas as pd
import plotly.express as px
from app.css_styling.style_page import css_styling
css_styling()


from utils.session_keys import DF_NEWS_TOPICS,DF_REDDIT_TOPICS,NEWS_TOPIC_KEYWORDS,REDDIT_TOPIC_KEYWORDS,TOPIC_SIMILARITY_DF,TOPIC_NARRATIVES

st.set_page_config(page_title="Question And Answer" , layout="wide")
st.title("News vs Reddit - Question and Anwers")

st.caption("Ask questions and explore answers from News and Reddit insights.")
st.write("")

all_keys = [DF_NEWS_TOPICS,DF_REDDIT_TOPICS,NEWS_TOPIC_KEYWORDS,REDDIT_TOPIC_KEYWORDS,TOPIC_SIMILARITY_DF,TOPIC_NARRATIVES]


for key in all_keys: 
    if key not in st.session_state: 
        st.session_state[key] = None

df_news = st.session_state.get(DF_NEWS_TOPICS)
df_reddit = st.session_state.get(DF_REDDIT_TOPICS)


