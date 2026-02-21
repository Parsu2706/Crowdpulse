import os 
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "models/gemini-2.0-flash"

sem = asyncio.Semaphore(2)

Narrative_prompt = """
You are a an analyst comparing media and public discourse. 
NEWS SUMMARY: 
{news_summary}
REDDIT SUMMARY: 
{reddit_summary}
SENTIMENT:
News: {news_sentiment}
Reddit: {reddit_sentiment}
TASK: 
Return ONLY bullet points. 
1.Agreements
2.Framing Differences
3. Reddit emphasis
4.News emphasis

LIMIT: 
- Max 180 words
- No intro 
- No conclusion

"""

async def generate_narrative(bundle): 
    prompt = Narrative_prompt.format(
        news_summary = bundle["news_summary"] , 
        reddit_summary = bundle['reddit_summary'] , 
        news_sentiment = bundle["news_sentiment"] ,
        reddit_sentiment = bundle['reddit_sentiment']
    )

    async with sem: 
        loop = asyncio.get_running_loop()
        for attempt in range(3): 
            try: 
                response = await loop.run_in_executor(None , lambda:client.models.generate_content(model=model , contents=prompt , config={'temperature': 0.2 , 'max_output_tokens': 450}))

                return {
                    "news_topic": bundle["news_topic"],
                    "reddit_topic": bundle["reddit_topic"],
                    "analysis": response.text.strip(),
                }
            except Exception as e : 
                if attempt == 2: 
                    raise 
                await asyncio.sleep(2)
                