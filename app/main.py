from fastapi import FastAPI, Request, Response, HTTPException
from app.api.api_v1.api import api_router_v1
from app.db import base  # Import base to register models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(api_router_v1, prefix="/api/v1")

# Dummy Endpoint
@app.get("/")
async def Insight_Ai():
   return "ShopGenie Python Backend By Nazmus Sakib"

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

