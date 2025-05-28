from langchain_groq import ChatGroq
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

def generate_responses(query: str):
    # Define prompt templates
    casual_template = """You're a helpful AI assistant. Provide a concise, casual explanation suitable for general audiences:
    Query: {query}
    Response:"""
    
    formal_template = """You're an academic expert. Provide a detailed, formal analysis with proper structure:
    Query: {query}
    Response:"""

    # Initialize Groq chat model
    llm = ChatGroq(temperature=0.7, model_name=MODEL_NAME, groq_api_key=GROQ_API_KEY)
    
    # Create chains
    casual_chain = (
        ChatPromptTemplate.from_template(casual_template)
        | llm
        | StrOutputParser()
    )
    
    formal_chain = (
        ChatPromptTemplate.from_template(formal_template)
        | llm
        | StrOutputParser()
    )
    
    # Generate responses
    casual_response = casual_chain.invoke({"query": query})
    formal_response = formal_chain.invoke({"query": query})
    
    return casual_response, formal_response