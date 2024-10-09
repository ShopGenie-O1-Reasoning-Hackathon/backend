import uuid
import csv
from typing import List, Optional
from sqlalchemy import (
    create_engine,
    Column,
    String,
    ARRAY,
    TIMESTAMP,
    UUID as SA_UUID,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from qdrant_client import QdrantClient
from qdrant_client.http.models import ScrollRequest
from qdrant_client.http import models
import os
# ==========================
# Configuration Parameters
# ==========================

QDRANT_URL=os.getenv("QDRANT_HOST")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")

QDRANT_COLLECTION = "InsightAI_shopgenie"  

# Scroll Parameters
SCROLL_BATCH_SIZE = 100  


def get_qdrant_client() -> QdrantClient:
    """
    Initialize and return the Qdrant client.
    """
    if QDRANT_API_KEY:
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    else:
        client = QdrantClient(url=QDRANT_URL)
    return client

# ==========================
# Data Retrieval from Qdrant
# ==========================
def retrieve_all_products_from_qdrant(client: QdrantClient, collection_name: str) -> List[dict]:
    """
    Retrieve all products from the specified Qdrant collection using the scroll API.

    Args:
        client (QdrantClient): The Qdrant client instance.
        collection_name (str): The name of the Qdrant collection.

    Returns:
        List[dict]: A list of product dictionaries.
    """
    products = []
    next_page_offset: Optional[str] = None

    while True:
        try:
            scroll_results = client.scroll(
                collection_name=collection_name, 
                limit=SCROLL_BATCH_SIZE,
                with_payload=True,
                with_vectors=False,
                offset=next_page_offset
            )
        except Exception as e:
            print(f"Error during scroll: {e}")
            break

        points = scroll_results[0]  
        next_page_offset = scroll_results[1] if len(scroll_results) > 1 else None

        if not points:
            break

        for item in points:
            product_data = item.payload
            normalized_product_data = {
                'id': str(item.id),  # Maps to 'id' in the table schema
                'link': product_data.get("Link", ''),
                'name': product_data.get("Name", ''),
                'gender': product_data.get("Gender", ''),
                'category': product_data.get("Category", ''),
                'company': product_data.get("Company", ''),
            }
            products.append(normalized_product_data)

        if not next_page_offset:
            break

    return products

# ==========================
# CSV Writing Function
# ==========================

def write_products_to_csv(products: List[dict], csv_file_name: str):
    """
    Write the list of products to a CSV file.

    Args:
        products (List[dict]): List of product dictionaries.
        csv_file_name (str): The name of the CSV file to create.
    """
    # Define the CSV columns based on the table schema
    fieldnames = ['id', 'link', 'name', 'gender', 'category', 'company']

    try:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write each product as a row in the CSV
            for product in products:
                writer.writerow(product)

        print(f"Successfully wrote {len(products)} products to '{csv_file_name}'.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# ==========================
# Main Execution
# ==========================
CSV_FILE_NAME = "products.csv"
def main():
    # Initialize Qdrant client
    client = get_qdrant_client()
    print("Connected to Qdrant.")

    # Retrieve all products from Qdrant
    print("Retrieving products from Qdrant...")
    try:
        products = retrieve_all_products_from_qdrant(client, QDRANT_COLLECTION)
        print(f"Retrieved {len(products)} products from Qdrant.")
    except Exception as e:
        print(f"Error retrieving products from Qdrant: {e}")
        return

    if not products:
        print("No products found in Qdrant. Exiting.")
        return

    # Write products to CSV
    print(f"Writing products to '{CSV_FILE_NAME}'...")
    try:
        write_products_to_csv(products, CSV_FILE_NAME)
    except Exception as e:
        print(f"Error during CSV writing: {e}")

if __name__ == "__main__":
    main()
