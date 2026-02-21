import streamlit as st
import plotly.express as px

from utils.data_loader import get_file_mtime
from utils.pipeline import load_and_preprocess
from services.sentiment_classification.infer import run_sentiment

from utils.session_keys import DF_REDDIT_TOPICS, DF_NEWS_TOPICS

from app.css_styling.style_page import css_styling

css_styling()

def cal_avg(df, label):
    vals = df.loc[df["label"] == label, "confidence"]
    return vals.mean() if not vals.empty else 0.0

st.session_state.setdefault(DF_REDDIT_TOPICS, None)
st.session_state.setdefault(DF_NEWS_TOPICS, None)
st.set_page_config(page_title="Sentiment Analysis" , layout="wide")
css_styling()


st.title("Sentiment Analysis")
st.sidebar.caption("Toggle between Reddit and News data")
toggle_bet_reddit_news = st.sidebar.toggle("Show Reddit Analysis" , value = True ,  key="reddit_news_toggle")

if toggle_bet_reddit_news: 
    st.subheader("Reddit Sentiment Analysis")
    st.info("Pick One or more subreddits , then run the model")
    tab1 , tab2 , tab3 = st.tabs(["Overview" , "Sentiment Overview" , "Labeled Data"])
    df_raw = load_and_preprocess(file_time=get_file_mtime(news=False) , news=False)
    if df_raw is None or df_raw.empty: 
        st.error("File Not Found")
        st.stop()

    def load_subreddits(path = "config/subreddits.txt"): 
        with open(path , "r") as f : 
            return [s.strip() for s in f if s.strip()]
    
    with tab1:
        subreddits = load_subreddits()
        selected_subs = st.multiselect("Pick subreddit to analyze" , options=subreddits )


        if st.button("Run Sentiment"  ,  key="reddit_sentiment_button"):
            if not selected_subs: 
                st.warning("Select at least one subreddit")
                st.stop()
            
            with st.spinner("Running Sentiment Analysis.."): 
                filtered = df_raw[df_raw['subreddit'].isin(selected_subs)]
                texts = filtered["model_text"].tolist()
                df_with_sentiment = run_sentiment(texts)
                df_with_sentiment['subreddit'] = filtered["subreddit"].values
                df_with_sentiment['text'] = filtered['model_text'].values
                st.session_state[DF_REDDIT_TOPICS] = df_with_sentiment
            st.success("Finished")
        st.divider()

        df_with_sentiment = st.session_state.get(DF_REDDIT_TOPICS)

        if df_with_sentiment is None:
            st.info("Run Sentiment analysis first")
            st.stop()

        df_with_sentiment = df_with_sentiment.copy()
        
        cols = st.columns(3)
        for col, label in zip(cols, ["POSITIVE", "NEGATIVE", "NEUTRAL"]):
            col.metric(
                f"{label} Avg Confidence",
                f"{cal_avg(df_with_sentiment, label):.3f}"
                )
            st.subheader("Top High confidence Posts")
            top_posts = (df_with_sentiment.sort_values("confidence" , ascending = False).groupby("label" , as_index = False).head(5))
            st.dataframe(top_posts , use_container_width=True)
        
    with tab2: 
  
        df = st.session_state.get(DF_REDDIT_TOPICS)

        if df is None:
            st.info("Run Sentiment analysis first")
            st.stop()
        df = df.copy()        
        if df is not None: 
            subs = sorted(df['subreddit'].unique())
            selected = st.multiselect("Filter by Subreddit" , subs , default=subs)
            df = df[df['subreddit'].isin(selected)]
            st.bar_chart(df['label'].value_counts())
            fig  = px.pie(df , names="label" , title="Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)

    with tab3: 

        
        df = st.session_state.get(DF_REDDIT_TOPICS)

        if df is None:
            st.info("Run Sentiment analysis first")
            st.stop()

        df = df.copy()     

        if df is not None: 
            sentiments = st.multiselect("Filter by sentiment" , sorted(df['label'].unique()))
            if sentiments : 
                df = df[df["label"].isin(sentiments)]
            df['text_preview'] = df['text'].str[:300]

            st.dataframe(
                df[["text_preview", "subreddit", "label", "confidence"]],
                use_container_width=True,height=500)
            st.download_button("Download labeled CSV",df.to_csv(index=False),"sentiment_label_data.csv")

else: 
    tab1 , tab2 , tab3 = st.tabs(["Overview" , "Sentiment Overview" , "Labeled Data"])
    df_raw = load_and_preprocess(file_time=get_file_mtime(news=True) , news=True)
    if df_raw is None or df_raw.empty: 
        st.error("File not found")
        st.stop()

    df_raw = df_raw.drop_duplicates("model_text")

    with tab1: 
        if st.button("Run Sentiment" , key='news_sentiment_button'):
            with st.spinner("Running Sentiment analysis.."): 
                    
                texts = df_raw["model_text"].tolist()
                df_sent_news = run_sentiment(texts)
                df_sent_news['text'] = df_raw["model_text"].values
                st.session_state[DF_NEWS_TOPICS] = df_sent_news
            st.success("Finished")

        df = st.session_state.get(DF_NEWS_TOPICS)

        if df is None:
            st.info("Run Sentiment analysis first")
            st.stop()
        df = df.copy()
        if df is None: 
            st.info("Run sentiment analysis first")
        else:  
            cols = st.columns(3)
            for col, label in zip(cols, ["POSITIVE", "NEGATIVE", "NEUTRAL"]):
                col.metric(
                    f"{label} Avg Confidence",
                    f"{cal_avg(df, label):.3f}"
                )

    with tab2: 
        
        df = st.session_state.get(DF_NEWS_TOPICS)
        if df is None:
            st.info("Run Sentiment analysis first")
            st.stop()

        df = df.copy()
        if df is not None: 
            st.bar_chart(df['label'].value_counts())
            fig = px.pie(df , names="label" , title="News Sentiment Distribution")
            st.plotly_chart(fig , use_container_width=True)

    with tab3: 
        df = st.session_state.get(DF_NEWS_TOPICS)

        if df is None:
            st.info("Run Sentiment analysis first")
            st.stop()
        df = df.copy()

        if df is not None:
            df['text_preview'] = df['text'].str[:300]

            st.dataframe(df , use_container_width=True , height=500)

            st.download_button("Download labeled news CSV",df.to_csv(index=False),"news_sentiment_labeled.csv")        