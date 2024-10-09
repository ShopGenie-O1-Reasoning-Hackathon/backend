from fastapi import APIRouter, Depends, HTTPException
from app.schemas.sentiment import SentimentAnalysis, SentimentRequest
from app.helpers.sentiment_analysis.sentiment_analysis import analyze_sentiment
router = APIRouter()

@router.post("/analyze_sentiment", response_model=SentimentAnalysis)
async def get_sentiment(request: SentimentRequest):
    try:
        result = analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


