import base64
import requests
from io import BytesIO
from fastapi import HTTPException
from app.core.openai import openaiClient


def download_image_as_base64(image_url: str) -> str:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        base64_image = base64.b64encode(image_data.read()).decode('utf-8')
        return base64_image
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image from the provided URL: {e}")


def generate_product_description(image_link:str, text_query:str):
    system_prompt = '''
        You are an AI that helps in describing products. You will be given two things
        - an image in base64 format
        - a text query
        A customer wants a similar product which is in the image, but has some additional requirements described in text query.
        generate a product description that not only matches the image but also fulfills the requirements described in text query. 
        Be precise and include all relevant specifications.
    '''
    try:
        base64_image = download_image_as_base64(image_link)
        response = openaiClient.chat.completions.create(
            model="gpt-4o-2024-08-06",  
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {    
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Describe the image in brief, highlighting all key features and relevant information points concisely. The product description must match the text query: {text_query}."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]   
                }
            ],
            max_tokens=200
        )
        print(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating image description: {e}")
        return "[Image description generation failed]"