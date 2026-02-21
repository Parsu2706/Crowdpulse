import streamlit as st
import asyncio
from services.news_reddit_summary.gemini_client import analyze_aligned_topics

@st.cache_data(show_spinner=False)
def cached_topic_analysis(bundle):
    return asyncio.run(analyze_aligned_topics(bundle))
