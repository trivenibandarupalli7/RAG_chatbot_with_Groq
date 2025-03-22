RAG Chatbot (PDF + Web) with Groq, FastAPI, and Chainlit
This is a simple RAG chatbot that lets you upload PDFs and ask questions. It uses Groq's LLM to answer using both PDF content and DuckDuckGo web search.

Tech Stack
Frontend: Chainlit

Backend: FastAPI

LLM: Groq API

Search: DuckDuckGo

Containerization: Docker + Docker Compose

How It Works
Upload PDFs in the chat.

Ask a question.

The bot breaks your question into sub-questions.

It looks for answers in the PDF or via web search.

Groq LLM generates a final response.

Run Locally
Add a .env file:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
SEARCH_API=duckduckgo
Build & start:

bash
Copy
Edit
docker-compose up --build
Chainlit: http://localhost:8001

FastAPI: http://localhost:8000

