from fastapi import APIRouter
from app.api.api_v1.endpoints import users,product_retrieve, product_search, sentiment_analysis,carts, reviews, clicks

api_router_v1 = APIRouter()

api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(product_retrieve.router, prefix="/product_retrieve", tags=["product_retrieve"])
api_router_v1.include_router(product_search.router, prefix="/product_search", tags=["product_search"])
api_router_v1.include_router(sentiment_analysis.router, prefix="/sentiment_analysis", tags=["sentiment_analysis"])
api_router_v1.include_router(carts.router, prefix="/cart", tags=["cart"])
api_router_v1.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router_v1.include_router(clicks.router, prefix="/clicks", tags=["clicks"])