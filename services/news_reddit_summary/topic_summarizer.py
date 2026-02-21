import os 
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "models/gemini-2.0-flash"
sem = asyncio.Semaphore(2)

summary_prompt = """
you are a highly concise analyst. 
summarize the following texts into Exactly 5 bullet points.
Rules: 
-max 120 words total
-No intro
-No conclusion 
-No fluff
-Focus on key facts , claims and themes/
TEXTS: {text}"""

async def summarize_texts(text_list): 
    joined= "\n".join(t[:1500] for t in text_list)
    prompt = summary_prompt.format(text = joined)
    async with sem: 
        loop = asyncio.get_running_loop()
        for attempt in range(3): 
            try: 
                response = await loop.run_in_executor(None , lambda: client.models.generate_content(model=model , contents=prompt , config={'temperature': 0.1 , "max_output_tokens": 250}))
                return response.text.strip()
            except Exception as e : 
                if attempt == 2 : 
                    raise
                await asyncio.sleep(2)

