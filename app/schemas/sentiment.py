
from pydantic import BaseModel, Field
from enum import Enum

class SentimentEnum(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class SentimentRequest(BaseModel):
    text: str = Field(description="The text to analyze for sentiment.")


class SentimentAnalysis(BaseModel):
    sentiment: SentimentEnum = Field(description="The detected sentiment of the text.")