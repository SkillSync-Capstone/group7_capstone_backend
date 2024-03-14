import os
import textwrap
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from IPython.display import display
from IPython.display import Markdown

import json

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def get_embedding(chunk):
    print(chunk)
    response = genai.embed_content(
    model="models/embedding-001",
    content=chunk,
    task_type="retrieval_document",
    title="Embedding for text")
    response_json = response
    return response_json

def get_llm_answer(prompt_template):
    model = genai.GenerativeModel("gemini-pro")
    print(prompt_template)
    response = model.generate_content(prompt_template)
    print(response.text)
    return response.text