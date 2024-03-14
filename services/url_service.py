import requests
from bs4 import BeautifulSoup
from services import gptService
from services import vectorStorageService
from utils.text_chunk import chunk_text
from utils.prompt_template import build_prompt
from services import text_service

PINECONE_INDEX_NAME = 'llm'


def process_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.find_all('p')
        extracted_text = ' '.join([text.get_text() for text in texts])

        chunks = chunk_text(extracted_text)
        vectorStorageService.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
        response_json = {
            "message": "Chunks embedded and stored successfully"
        }
        return response_json
    else:
        return {"error": f"Failed to retrieve the URL, status code: {response.status_code}"}, 400
