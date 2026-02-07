import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_model():
    provider = os.getenv("MODEL_PROVIDER","groq")
    if provider=="groq":
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
    else:
        raise ValueError("Invalid MODEL_PROVIDER")