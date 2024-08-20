# Custom ChatBot with History 

This repository contains a FastAPI-based chatbot application that can handle user questions, provide responses based on a knowledge base, and maintain a conversation history. The application also includes an option to reset the conversation history.

## Features

- **POST /ask**: Handles user questions, interacts with a chatbot system, and provides appropriate responses.
- **GET /**: Returns a welcome message when accessing the root endpoint.

## Folder Structure

```plaintext
app/
├── chatbot/
│   ├── chatbot.py               # Core chatbot logic, including the setup of RAG system with history
│   ├── __init__.py              # Initialization file for the chatbot module
│   ├── __pycache__/             # Cached Python files
├── database_prep/
│   ├── database_preparation.py   # Database preparation logic
│   ├── Extraction.py             # Extraction logic
│   ├── __init__.py               # Initialization file for the database preparation module
│   ├── __pycache__/              # Cached Python files
├── __pycache__/                  # Cached Python files
├── data/
│   ├── collated_text.txt         # Data file with extracted information
│   ├── summary.txt               # Summary data used for the chatbot
├── text/                         # Additional text data
├── .dockerignore                 # Specifies files and directories to be ignored by Docker
├── .gitignore                    # Specifies files and directories to be ignored by Git
├── api.py                        # Main FastAPI application with API endpoints
├── Dockerfile                    # Dockerfile for building the Docker image
├── entrypoint.sh                 # Entrypoint script for Docker container
├── heroku.yml                    # Heroku configuration file for deployment
├── README.md                     # Documentation for the repository
├── requirements.txt              # Python dependencies
```

## API Endpoints

### 1. **POST /ask**

#### Description:
Handles the POST request to the `/ask` endpoint.

This function processes the user's question, interacts with the chatbot system, and returns a response. If the user inputs `'reset'`, it clears the chat history.

#### Request Body:
- `question`: A string representing the user's question.

#### Response:
- **200 OK**: Returns a response with the chatbot's answer to the user's question or a reset confirmation.

#### Example:
```json
{
  "question": "Who are you?"
}
```

#### Example Response:
```json
{
  "response": "I am an intelligent assistant designed to guide users through tasks and provide information."
}
```

#### Special Behavior:
- If the user enters `"reset"` as the question, the chatbot's conversation history is cleared, and the response indicates that the history has been reset.

#### Raises:
- **HTTPException (500)**: If an error occurs while processing the request.

### 2. **GET /**

#### Description:
Handles the GET request to the root (`/`) endpoint.

This function returns a welcome message when the root endpoint is accessed.

#### Response:
- **200 OK**: Returns a dictionary containing a welcome message and a health check status.

#### Example Response:
```json
{
  "message": "Welcome to the ChatBot with History API!",
  "health_check": "OK"
}
```

## Deployment

### Docker

To build and run the application locally using Docker:

1. **Build the Docker Image:**
   ```bash
   docker build -t chatbot .
   ```

2. **Run the Docker Container Locally:**
   ```bash
   docker run -p 8080:8080 chatbot
   ```

### Heroku

To deploy the application on Heroku, ensure you have the `heroku.yml` and `Dockerfile` set up properly, and push your code to Heroku using the `git push heroku main` command.

## Requirements

- **Python 3.9**
- **FastAPI**
- **Uvicorn**
- **Docker**
- **LangChain**
- **Heroku CLI** (for Heroku deployment)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rohithsiddhartha/Chatbot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd CustomChatBot
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn api:app --reload
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
