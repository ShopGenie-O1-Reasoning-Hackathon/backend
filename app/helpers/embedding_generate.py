
from app.core.openai import openaiClient
from app.core.roboflow import roboflow_client
from fastapi import FastAPI, HTTPException
#################################################################################################
#   Helper function to get the vector embedding for any text
#   input: string, output: multidimensional array representing embedding
#   vector dimension size = 3072
#################################################################################################
def get_text_embedding(txt):
    embedding_model = "text-embedding-3-large"
    str_embedding = openaiClient.embeddings.create(input= txt, model=embedding_model)
    return str_embedding.data[0].embedding

def get_image_embeddings(image_link: str):
    try:
        print(image_link)
        res = roboflow_client.get_clip_image_embeddings(inference_input=image_link, clip_version="ViT-B-32")
        embeddings = res["embeddings"][0]
        return embeddings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))