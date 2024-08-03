import json
import openai
import os
from dotenv import load_dotenv

# Load the JSON file
with open('Extracted data.json', 'r') as file:
    data = json.load(file)

# Display the loaded data
for item in data:
    print(f"Title: {item['title']}")
    print(f"Summary: {item['summary']}")
    print(f"Date: {item['date']}\n")


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get embeddings
def get_embeddings(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Create embeddings for each data item
for item in data:
    item['embedding'] = get_embeddings(item['summary'])


import faiss
import numpy as np

# Create a FAISS index
embedding_dim = len(data[0]['embedding'])
index = faiss.IndexFlatL2(embedding_dim)

# Prepare the data for FAISS
embeddings = np.array([item['embedding'] for item in data]).astype('float32')
index.add(embeddings)

# Save the index
faiss.write_index(index, "embeddings.index")
