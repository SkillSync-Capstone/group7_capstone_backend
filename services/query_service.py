from flask import request, jsonify
from services.vectorStorageService import get_most_similar_chunks_for_query
from utils.prompt_template import build_prompt
from services.gptService import get_llm_answer
import os
import openai
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import constants
load_dotenv()
os.getenv("OPENAI_API_KEY")
PINECONE_INDEX_NAME = 'llm'

def handle_query(query):
        context_chunks = get_most_similar_chunks_for_query(query, PINECONE_INDEX_NAME)
        print(context_chunks)
        prompt = build_prompt(query, context_chunks)
        
        print("\n==== PROMPT ====\n",prompt)
        answer = get_llm_answer(prompt)
        return answer 


def handle_new_query(query, PERSIST=False):
    # Initialize the index based on the persistence flag
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = DirectoryLoader("docs/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    if query.lower() in ['quit', 'q', 'exit']:
        return {"error": "Query to exit received."}
    
    result = chain({"question": query, "chat_history": []})
    
    return {"answer": result['answer']}

        