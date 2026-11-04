import json
import requests
from typing import Literal
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException, Field
from pydantic import BaseModel

app = FastAPI()


class EchoRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
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
    except requests.ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Can't reach Ollama. Is it running?",
        ) from exc
    except requests.Timeout as exc:
        raise HTTPException(
            status_code=503,
            detail="Can't reach Ollama. Is it running?",
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Ollama returned an invalid response") from exc

    if response.status_code >= 400:
        message = data.get("error", response.text) if isinstance(data, dict) else response.text
        raise HTTPException(status_code=502, detail=f"Ollama error: {message}")

    try:
        reply = data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="Ollama returned an invalid response") from exc
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
