def align_topic_to_text(similarity_df , df_news , df_reddit , top_k = 5 , max_texts_per_side = 8): 
    corpus = []
    top_pairs = similarity_df.head(top_k)
    for row in top_pairs.itertuples(index=False): 
        reddit_topic = row._0 if hasattr(row, "_0") else getattr(row, "Reddit_Topic")
        news_topic = row._1 if hasattr(row, "_1") else getattr(row, "Closest_News_Topic")
        if news_topic == "—":
            continue

        filtered_reddit = df_reddit[df_reddit["topic_name"] == reddit_topic]
        filtered_news = df_news[df_news["topic_name"] == news_topic]
        if filtered_reddit.empty or filtered_news.empty:
            continue

        reddit_texts = filtered_reddit.sample(
            n=min(max_texts_per_side, len(filtered_reddit)),
            random_state=42
        )

        news_texts = filtered_news.sample(
            n=min(max_texts_per_side, len(filtered_news)),
            random_state=42
        )
        corpus.append(
            {
                "reddit_topic": reddit_topic,
                "news_topic": news_topic,
                "reddit_texts": reddit_texts["text"].tolist(),
                "news_texts": news_texts["text"].tolist(),
                "reddit_sentiment": reddit_texts["label"].value_counts(normalize=True).to_dict(),
                "news_sentiment": news_texts["label"].value_counts(normalize=True).to_dict(),
            }
        )

    return corpus
