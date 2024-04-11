from PyPDF2 import PdfReader
from services import gptService
from services import vectorStorageService
from utils.text_chunk import chunk_text
from services import text_service
from typing_extensions import Concatenate
from langchain.text_splitter import CharacterTextSplitter
from flask import Flask, request, jsonify
import fitz  
import os
from docx import Document


PINECONE_INDEX_NAME = 'llm'
DOCX_FILES_DIRECTORY = "docs/"

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


def get_file_size(file):
    """
    Gets the file size of a given file object by reading its stream.
    :param file: File object.
    :return: File size in bytes.
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size
def extract_text_and_create_docx(pdf_file, docx_filename):
    """
    Extracts text from a PDF file object and saves it to a .docx file in the specified directory.
    :param pdf_file: PDF file object.
    :param docx_filename: Filename for the .docx file.
    """
    text = ''
    pdf_file.seek(0)
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        document = Document()
        for page in doc:
            text = page.get_text()
            document.add_paragraph(text)
        # Ensure the directory exists
        os.makedirs(DOCX_FILES_DIRECTORY, exist_ok=True)
        # Save the .docx file in the specified directory
        full_path = os.path.join(DOCX_FILES_DIRECTORY, docx_filename)
        document.save(full_path)
    pdf_file.seek(0)  # Reset the PDF file position if needed

def upload_file(file, filename):
    """
    Processes the PDF file object, extracts its details, including text, and saves the text to a .docx file in a specified directory.
    :param file: PDF file object.
    :param filename: Name of the file.
    :return: Dictionary with confirmation message, file details, and path to the .docx file.
    """
    file_size = get_file_size(file)
    # Creating a docx filename based on the original PDF filename
    docx_filename = f"{os.path.splitext(filename)[0]}.docx"
    extract_text_and_create_docx(file, docx_filename)
    
    file_details = {
        "Filename": filename,
        "File size": file_size,
        "Docx File": os.path.join(DOCX_FILES_DIRECTORY, docx_filename)  # Provide the full path in the response
    }
    
    confirmation_message = f"File '{filename}' processed successfully and saved as '{docx_filename}' in the specified directory."
    return {"message": confirmation_message, "file_details": file_details}