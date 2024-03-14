from flask import request, jsonify
from services import gptService
from services import vectorStorageService

from utils.text_chunk import chunk_text
from utils.prompt_template import build_prompt
from services import text_service


PINECONE_INDEX_NAME = 'llm'



def process_text(text):
    chunks = chunk_text(text)
    print(chunks)
    vectorStorageService.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return response_json
