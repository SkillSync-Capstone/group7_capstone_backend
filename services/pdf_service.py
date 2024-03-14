from PyPDF2 import PdfReader
from services import vectorStorageService
from utils.text_chunk import chunk_text
from services import llmService,text_service
from typing_extensions import Concatenate

PINECONE_INDEX_NAME = 'llm'

def handle_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    raw_text = ''
    for i, page in enumerate(pdf.pages):
     content = page.extract_text()
    if content:
        raw_text += content
        
    chunks = chunk_text(raw_text)
    vectorStorageService.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return response_json
        
