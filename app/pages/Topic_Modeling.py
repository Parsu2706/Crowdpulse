import streamlit as st
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

from services.topic_modeling.infer import train_and_infer
from services.topic_modeling.utils import generate_topic_title
from utils.session_keys import DF_REDDIT_TOPICS,DF_NEWS_TOPICS,NEWS_TOPIC_KEYWORDS,REDDIT_TOPIC_KEYWORDS,TOPIC_SIMILARITY_DF,TOPIC_NARRATIVES 
st.set_page_config(page_title="Topic Modeling" , layout="wide")
st.title("Topic Modeling")
st.caption("Discover what people are talking about")
st.divider()


all_keys = [DF_REDDIT_TOPICS,DF_NEWS_TOPICS,NEWS_TOPIC_KEYWORDS,REDDIT_TOPIC_KEYWORDS,TOPIC_SIMILARITY_DF,TOPIC_NARRATIVES]
for key in all_keys: 
    if key not in st.session_state: 
        st.session_state[key] = None

if "TOPIC_TITLES" not in st.session_state:
    st.session_state["TOPIC_TITLES"] = None

def load_more_stopwords(path = "stopwords.txt")-> set[str]: 
    with open(path , "r" , encoding="utf-8") as f : 
        return {line.strip().lower() for line in f if line.strip()}
    
stopwords = STOPWORDS.union(load_more_stopwords())
st.sidebar.caption("Choose data source")
use_reddit = st.sidebar.toggle("Use Reddit Data" , value=True ,key="topic_use_reddit_toggle")

SESSION_KEY = DF_REDDIT_TOPICS if use_reddit else DF_NEWS_TOPICS
KEYWORDS_KEY = REDDIT_TOPIC_KEYWORDS if use_reddit else NEWS_TOPIC_KEYWORDS

df  = st.session_state.get(SESSION_KEY)

if df is None: 
    st.warning("Please run Sentiment Analysis first before topic modeling")
    st.stop()

if use_reddit and "subreddit" in df.columns: 
    subreddits = sorted(df['subreddit'].dropna().unique())
    selected_subs = st.multiselect("Filter by subreddit" , subreddits , default= subreddits)
    if not selected_subs: 
        st.warning("Select atleast one subreddit")
        st.stop()

    df = df[df['subreddit'].isin(selected_subs)]
if len(df) < 20 : 
    st.warning("Not Enough data for topic modeling ")
    st.stop()
max_samples = min(400 , len(df))
with st.form("Topic Model Form"): 
    size = max(120 , int(len(df) * 0.6))
    size = min(size , max_samples)

    n_samples = st.slider("Number of text to analyze" , min_value=50 , max_value=max_samples , value=size)
    submitted = st.form_submit_button("Run Topic Modeling")

if submitted : 
    with st.spinner("Running topic modeling.."): 
        if len(df) > n_samples :
            sampled = df.sample(n = n_samples , random_state = 42)
        else: 
            sampled = df
        texts = sampled['text'].tolist()
        topic_df , topic_keywords = train_and_infer(text=texts)
        topic_titles = {topic_id: generate_topic_title(", ".join(words)) for topic_id , words in topic_keywords.items()}
        topic_df['topic_name'] = topic_df['topic'].map(topic_titles)
        st.session_state["TOPIC_TITLES"] = topic_titles
        base_df = st.session_state[SESSION_KEY]
        if base_df is None:
            st.warning("Sentiment data missing.")
            st.stop()

        base_df = base_df.copy()
        merged = base_df.merge(topic_df[["text", "topic", "topic_name"]],on="text",how="left")
        st.session_state[SESSION_KEY] = merged
        st.session_state[KEYWORDS_KEY] = topic_keywords        
        st.session_state[TOPIC_SIMILARITY_DF] = None
        st.session_state[TOPIC_NARRATIVES] = None

    st.success("Topic Modeling Complete")

df = st.session_state.get(SESSION_KEY)
topic_keywords = st.session_state[KEYWORDS_KEY]
topic_titles = st.session_state.get("TOPIC_TITLES", {})


if df is None or "topic" not in df.columns: 
    st.info("Run topic modeling to see results.")
    st.stop()

if topic_keywords is None: 
    st.stop()


st.subheader("Topic Summary")

for topic_id , words in topic_keywords.items(): 
    topic_name = topic_titles.get(topic_id, f"Topic {topic_id}")
    with st.expander(f"Topic {topic_id}: {topic_name}"): 
        st.markdown("**Top Words**")
        st.write(", ".join(words))

st.subheader("Topic Assignment")
topic_view = df.dropna(subset = ['topic'])
st.dataframe(topic_view[["text" , "topic" , "topic_name"]] , use_container_width=True)

availabel_topics = sorted(topic_view['topic'].unique())
selected_topic = st.selectbox("Select Topic to Visualize" , options=availabel_topics)
topic_texts = topic_view[topic_view["topic"] == selected_topic]["text"]

if len(topic_texts) > 0 : 
    combined_text = " ".join(topic_texts)
    wordcloud = WordCloud(width=900 , height=450 , background_color="white" , stopwords=stopwords , collocations=False).generate(combined_text)
    fig , ax = plt.subplots(figsize = (11 , 5))
    ax.imshow(wordcloud , interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)

else: 
    st.info("Not Enough text to visualize this topic.")