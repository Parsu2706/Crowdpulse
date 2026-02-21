import streamlit as st
import pandas as pd
import spacy
from collections import Counter
from app.css_styling.style_page import css_styling

from utils.session_keys import DF_NEWS_TOPICS, DF_REDDIT_TOPICS

st.set_page_config(page_title="Entity Frequency Analysis", layout="wide")
css_styling()
st.title("Most Discussed Entities Across Platforms")
st.caption("Discover the entities capturing the most attention across media and online communities.")
st.write("")
@st.cache_resource
def load_model():
    return spacy.load('en_core_web_sm')
model = load_model()


@st.cache_data
def extract_entities(text): 
    ner_label = {"GPE" , "ORG" , "PERSON" , "NORP"}
    counter = Counter()
    for doc in model.pipe(text.astype(str) , batch_size=50): 
        for ent in doc.ents: 
            if ent.label_ in ner_label: 
                entity = ent.text.strip()

                if len(entity) > 2: 
                    counter[entity] += 1
    return counter

df_news = st.session_state.get(DF_NEWS_TOPICS)
df_reddit = st.session_state.get(DF_REDDIT_TOPICS)

if df_news is None or df_reddit is None:
    st.warning("Run sentiment analysis first so data is available.")
    st.stop()

news_text_col = "text" if "text" in df_news.columns else "model_text"
reddit_text_col = "text" if "text" in df_reddit.columns else "model_text"

with st.spinner("Extracting entities..."): 
    news_count = extract_entities(df_news[news_text_col])
    reddit_count = extract_entities(df_reddit[reddit_text_col])


entities = set(news_count) | set(reddit_count)
rows = []

for ent in entities: 
    news_val = news_count.get(ent  , 0)
    reddit_val = reddit_count.get(ent , 0 )
    total = news_val + reddit_val
    if total < 5 : 
        continue 
    
    rows.append({
        "Entity" : ent , 
        "Reddit Mentions" : reddit_val , 
        "News Mention" : news_val , 
        "Gap (Reddit - News)" : reddit_val - news_val , 
        "Total Mentions" : total
    })

new_entity_df = pd.DataFrame(rows).sort_values("Total Mentions" , ascending=False).reset_index(drop=True)

with st.container(border=True):
    top_n = st.slider("Show Top Entities" , 10 , 50 , 20)

display_df = new_entity_df.head(top_n)

st.dataframe(display_df , use_container_width=True)


st.write("")
st.write("")


chart_df = display_df.set_index("Entity")[["Reddit Mentions", "News Mention"]]

st.bar_chart(chart_df)

st.download_button("Download Entity Counts" , new_entity_df.to_csv(index=False) , file_name="entity_frequency.csv")
