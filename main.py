from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from db import init_db
from routers import chat, tickets
from services.classifier import _openai_client  # only for health flag


app = FastAPI(title="Bank Support Multi-Agent MVP")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True, "openai_enabled": _openai_client is not None}

app.include_router(chat.router)
app.include_router(tickets.router)
