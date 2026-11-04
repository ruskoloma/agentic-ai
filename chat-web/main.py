import json
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class EchoRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(request: EchoRequest):
    return {"message": request.message, "length": len(request.message)}


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
