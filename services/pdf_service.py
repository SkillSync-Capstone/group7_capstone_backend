from PyPDF2 import PdfReader
from services import gptService
from services import vectorStorageService
from utils.text_chunk import chunk_text
from services import text_service
from typing_extensions import Concatenate
from langchain.text_splitter import CharacterTextSplitter

PINECONE_INDEX_NAME = 'llm'

def handle_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    raw_text = ''
    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
         raw_text += content
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
    texts = text_splitter.split_text(raw_text)
        
#    chunks = chunk_text(raw_text)
    vectorStorageService.embed_chunks_and_upload_to_pinecone(texts, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return response_json
        
