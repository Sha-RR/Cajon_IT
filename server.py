from dotenv import load_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}

@app.post("/api/chat")
def chat(req: ChatRequest):
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=req.message
    )
    return {"response": resp.output_text}