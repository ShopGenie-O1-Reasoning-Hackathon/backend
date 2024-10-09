
from app.core.openai import openaiClient
from app.schemas.sentiment import SentimentEnum, SentimentAnalysis

def analyze_sentiment(text: str) -> SentimentAnalysis:
    system_prompt='''
        You are a helpful assistant. You analyze the sentiment from user-feedback on a product. Sentiment can be positive, negative or neutral
    '''

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=SentimentAnalysis,
    )

    return completion.choices[0].message.parsed

    sentiments = list(SentimentEnum)
    sentiment = random.choice(sentiments)
    confidence = random.uniform(0.7, 1.0)
    
    return SentimentAnalysis(
        text=text,
        sentiment=sentiment,
        confidence=confidence
    )