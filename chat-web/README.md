# chat-web — Ruslan Kolomiyets, DVOP311

A FastAPI app with health, echo, local model listing, and chat routes.

From the `chat-web` directory, activate the virtual environment, install dependencies with `pip install -r requirements.txt`, and run `uvicorn main:app --reload`. Open http://127.0.0.1:8000/docs to try the routes.

`/models` and `/chat` require a running Ollama server; `/chat` defaults to `llama3.2:3b`.
