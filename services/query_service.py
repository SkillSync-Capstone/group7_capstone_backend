from flask import request, jsonify
from services.vectorStorageService import get_most_similar_chunks_for_query
from utils.prompt_template import build_prompt
#from services.geminiService import get_llm_answer
from services.gptService import get_llm_answer



PINECONE_INDEX_NAME = 'llm'

def handle_query(query):
        context_chunks = get_most_similar_chunks_for_query(query, PINECONE_INDEX_NAME)
        print(context_chunks)
        prompt = build_prompt(query, context_chunks)
        print("\n==== PROMPT ====\n")
        answer = get_llm_answer(prompt)
        return answer 
