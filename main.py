from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.utils import preprocess_pdf as process_pdf
from app.rag import query_processor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = {}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text_chunks = process_pdf(contents)
        vector_store[file.filename] = text_chunks
        return JSONResponse(content={"message": "PDF processed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(query: dict):
    try:
        result = query_processor(query["message"], vector_store)
        return JSONResponse(content={"answer": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))