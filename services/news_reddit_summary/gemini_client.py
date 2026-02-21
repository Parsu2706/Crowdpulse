import asyncio
from services.news_reddit_summary.topic_summarizer import summarize_texts
from services.news_reddit_summary.narrative_generator import generate_narrative

async def run_topic_pipeline(full_text): 
    news_summary = await summarize_texts(full_text['news_texts'])
    reddit_summary = await  summarize_texts(full_text['reddit_texts'])
    bundle = {**full_text , "news_summary" : news_summary , "reddit_summary" : reddit_summary}
    return await generate_narrative(bundle=bundle)

async def analyze_aligned_topics(bundle): 
    bundle = bundle[:3]
    tasks = [run_topic_pipeline(f) for f in bundle]
    results = await asyncio.gather(*tasks , return_exceptions=True)
    cleaned = []
    for res in results: 
        if isinstance(res , Exception): 
            cleaned.append({
                "news_topic": "Error",
                "reddit_topic": "Error",
                "analysis": f"Failed: {res}"}) 
        else: 
            cleaned.append(res)
    return cleaned


