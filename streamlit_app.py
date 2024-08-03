# streamlit_app.py
import streamlit as st
import faiss
import numpy as np
import os
from dotenv import load_dotenv
import openai
import json

# Load the data and FAISS index
with open('Extracted data.json', 'r') as file:
    data = json.load(file)

index = faiss.read_index("embeddings.index")

# OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get embeddings
def get_embeddings(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Streamlit app
st.title("News Article Chatbot")

query = st.text_input("Enter your query:")
search_button = st.button("Search")

if search_button and query:
    query_embedding = np.array(get_embeddings(query)).astype('float32')
    D, I = index.search(np.array([query_embedding]), k=5)
    
    relevant_articles = [data[i] for i in I[0]]
    
    # Generate a response using GPT-4
    context = "\n\n".join([f"Title: {article['title']}\nSummary: {article['summary']}\nDate: {article['date']}" for article in relevant_articles])
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Based on the following articles, answer the query: {query}\n\n{context}"}
        ],
        max_tokens=200
    )
    
    st.write(response['choices'][0]['message']['content'])
