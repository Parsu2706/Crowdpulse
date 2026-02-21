import streamlit as st
import pandas as pd
import os
from datetime import datetime
from config.paths import REDDIT_CSV , NEWS_CSV
from scrapers.news_scraper import fetch_news_article
from scrapers.reddit_scraper import run_scrapper
from app.css_styling.style_page import css_styling, metric_card



st.set_page_config(page_title="CrowdPulse", layout="wide")
css_styling()


SUBREDDIT_FILE = "config/subreddits.txt"

def load_subs_from_txt(): 
    if not os.path.exists(SUBREDDIT_FILE): 
        return []
    with open(SUBREDDIT_FILE , "r") as f : 
        return [line.strip() for line in f if line.strip()]
    
def save_subs_to_txt(sub): 
    os.makedirs(os.path.dirname(SUBREDDIT_FILE) , exist_ok=True)
    with open(SUBREDDIT_FILE , "w") as f : 
        f.write("\n".join(sorted(set(sub))))


st.markdown("""
<div class= "main_title">CrowdPulse</div>
<div class ="subtitle">Real-time intelligence from <b>Reddit + Global News</b><br>  
Track emerging trends, public sentiment, and high-impact discussions — all in one place.</div>
""" , unsafe_allow_html=True)

st.write("")
st.sidebar.markdown("### Data Controls")
if st.sidebar.button("Fetch Reddit Data"):
    with st.spinner("Fetching Reddit data..."):
        try: 
            run_scrapper()
            st.cache_data.clear()
            st.success("✅ Reddit data fetched successfully")
            st.rerun() 
        except Exception as e:
            st.error(f"Reddit fetch failed: {e}")
if st.sidebar.button("Fetch News Data"):
    with st.spinner("Fetching News data..."):
        try: 
            fetch_news_article()
            st.cache_data.clear()
            st.success("News data fetched successfully")
            st.rerun() 
        except Exception as e:
            st.error(f"News fetch failed: {e}")

st.markdown("""<div class ="section-header" >Platforms Overview</div>""" ,unsafe_allow_html=True)
if os.path.exists(REDDIT_CSV) and os.path.exists(NEWS_CSV): 
    reddit_df = pd.read_csv(REDDIT_CSV)
    news_df = pd.read_csv(NEWS_CSV)
    col1 , col2 , col3 , col4 = st.columns(4)
    with col1:
        metric_card("Total Reddit Posts" , len(reddit_df))
    with col2: 
        metric_card("Total News Articles" , len(news_df))
    with col3:
        metric_card("Total Data Points" , len(reddit_df) + len(news_df))
    with col4:
        metric_card("Tracked Subreddits" , reddit_df['subreddit'].nunique())
else: 
    st.warning("Dataset Not Found . Fetch data from sidebar")

st.write("")

allcurrent_subs = load_subs_from_txt()
if allcurrent_subs is None: 
    st.warning("Error occur because no subreddit available , Please add some subreddits")

st.markdown("""<div class="section-header" >Manage subreddits</div>""" , unsafe_allow_html=True)
col1 , col2 = st.columns(2)
with col1: 
    add_subreddit = st.text_input("Add subreddits",placeholder="datascience")

    if st.button("Add Subreddits"): 
        addedsubs = [s.strip().lower().replace("r/", "") for s in add_subreddit.split(",") if s.strip()]
        save_subs_to_txt(allcurrent_subs + addedsubs)
        st.success("Subreddits added ✅")
        st.rerun()
with col2:
    if allcurrent_subs: 
        removeSubreddits = st.multiselect("Remove subreddits" , allcurrent_subs)
        if st.button("Remove selected Subreddits "): 
            remaining = [s for s in allcurrent_subs if s not in removeSubreddits]
            save_subs_to_txt(remaining)
            st.success("Subreddits removed ✅")
            st.rerun()


