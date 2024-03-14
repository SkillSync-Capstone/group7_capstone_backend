import os
from pinecone import Pinecone, Index, ServerlessSpec
#from services.geminiService import get_embedding
from services.gptService import get_embedding

import json

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY') 
print(PINECONE_API_KEY)
pinecone_client = Pinecone(api_key=PINECONE_API_KEY,environment='gcp-starter')


#EMBEDDING_DIMENSION = 768
#EMBEDDING_DIMENSION = 1536
EMBEDDING_DIMENSION = 3072



def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    print(index_name)
    
    if index_name in [index['name'] for index in pinecone_client.list_indexes().indexes]:
        print("\nIndex already exists. Deleting index ...")
        pinecone_client.delete_index(name=index_name)

    
    print("\nCreating a new index: ", index_name)
    if not index_name:
     raise ValueError("Index name must be specified")

    pinecone_client.create_index(
        name=index_name,
        dimension=EMBEDDING_DIMENSION, 
        metric='cosine',
         spec=ServerlessSpec(
        cloud='aws', 
        region='us-west-2'
    )
    )

    # Connect to the index
    index = pinecone_client.Index(index_name)

    print("\nEmbedding chunks  ...")
    embeddings_with_ids = []
    print(chunks)
    for i, chunk in enumerate(chunks):
        if not chunk: 
          continue
    embedding = get_embedding(chunk)
    print(embedding["embedding"])
    embeddings_with_ids.append((str(i), embedding["embedding"], {"chunk_text": chunk}))

    print("\nUploading chunks to Pinecone ...")
    # Perform the upsert operation
    index.upsert(embeddings_with_ids)

    print(f"\nUploaded {len(chunks)} chunks to Pinecone index '{index_name}'.")

def get_most_similar_chunks_for_query(query, index_name):
    print("\nEmbedding query  ...")
    question_embedding = get_embedding(query)
    embeddings = question_embedding["embedding"]
    print(embeddings)

    print("\nQuerying Pinecone index ...")
    index = pinecone_client.Index(index_name)
    query_results = index.query(vector=[embeddings], top_k=5,include_metadata=True)

    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks


def delete_index(index_name):
    pinecone_client.delete_index(name=index_name)
    print(f"Index {index_name} deleted successfully")
