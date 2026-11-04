import json
from typing import Literal
from urllib.error import URLError
from urllib.request import urlopen

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class EchoRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_items=1)
    model: str = "llama3.2:3b"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(request: EchoRequest):
    return {"message": request.message, "length": len(request.message)}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": request.model,
                "messages": [message.dict() for message in request.messages],
                "stream": False,
            },
            timeout=60,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail="Can't reach Ollama. Is it running?",
        ) from exc

    if not response.ok:
        try:
            error = response.json().get("error")
        except (ValueError, AttributeError):
            error = None
        error = error or response.text or "Unknown Ollama error"
        raise HTTPException(status_code=502, detail=f"Ollama error: {error}")

    try:
        reply = response.json()["message"]["content"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail="Ollama error: Invalid response")

    return {"reply": reply, "model": request.model}


@app.get("/models")
def models():
    try:
        with urlopen("http://localhost:11434/api/tags", timeout=5) as response:
            data = json.load(response)
        names = [model["name"] for model in data["models"]]
        if not all(isinstance(name, str) for name in names):
            raise ValueError("Invalid model names")
    except (URLError, OSError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable or returned an invalid response. Ensure Ollama is running.",
        ) from exc
    return {"models": names}
