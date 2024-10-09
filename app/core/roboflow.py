from inference_sdk import InferenceHTTPClient
from app.core.config import settings

roboflow_client = InferenceHTTPClient(
    api_url="https://infer.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY,
)