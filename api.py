import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chatbot.chatbot import create_vector_store, setup_rag_with_history, get_response 

os.environ["OPENAI_API_KEY"] = "sk-"

app = FastAPI()

# Load the text and summary once when the app starts
with open('data/collated_text.txt', 'r') as file:
    extracted_info = file.read()

with open('data/summary.txt', 'r') as file:
    summary = file.read()

# Create vector store
vector_store = None

def initialize_vector_store():
    global vector_store
    vector_store = create_vector_store(extracted_info)

# Ensure vector store is initialized
initialize_vector_store()

# Setup RAG system with chat history
qa_system = setup_rag_with_history(vector_store, summary)

# Define request/response models
class QueryRequest(BaseModel):
    question: str
    class Config:
        schema_extra = {
            "example": {
                "question": "Who are you?"
            }
        }

class QueryResponse(BaseModel):
    response: str
    class Config:
        schema_extra = {
            "example": {
                "response": "I am an intelligent assistant designed to guide users through tasks and provide information on various topics. Specifically, I am here to assist with questions related to Artisan AI, an AI-first platform that revolutionizes outbound sales automation. If you have any specific questions or tasks related to Artisan AI or any other topic, feel free to ask, and I'll be happy to help!"
            }
        }

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Handles the POST request to the /ask endpoint.

    This function processes the user's question, interacts with the chatbot system, 
    and returns a response. If the user inputs 'reset', it clears the chat history.

    Args:
        request (QueryRequest): The user's question in a POST request.

    Returns:
        QueryResponse: The chatbot's response to the user's question or a reset confirmation.

    Special Behavior:
        - If the user enters "reset" as the question, the chatbot's conversation 
          history is cleared, and the response indicates that the history has been reset.

    Raises:
        HTTPException: If an error occurs while processing the request.
    """
    try:
        user_question = request.question
        if user_question.lower() == 'reset':
            qa_system["memory"].clear()
            return QueryResponse(response="Chat history has been reset.")
        
        response = get_response(qa_system, user_question)
        return QueryResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    """
    Handles the GET request to the root ("/") endpoint.

    This function returns a welcome message when the root endpoint is accessed.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to the ChatBot with History API!", "health_check": "OK"}
