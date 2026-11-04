# Spec: POST /chat

## Goal
Let a client send a conversation to a local Ollama model and receive its next reply. This gives chat-web a stateless API for multi-turn conversations.

## Request
POST /chat with JSON:
{"messages": [{"role": "user", "content": "hi"}], "model": "llama3.2:3b"}

- messages: the whole conversation so far, oldest first. Each item has role and content. Required, with at least one item.
- model: optional; defaults to llama3.2:3b.

## Response
200 with JSON: {"reply": "<the model's answer>", "model": "<model used>"}

## Errors
- messages missing or empty → 422 (FastAPI's validation error)
- Ollama not running → 503 {"detail": "Can't reach Ollama. Is it running?"}
- Ollama answers with an error (for example, the model isn't installed) → 502 {"detail": "Ollama error: <Ollama's message>"}

## Constraints
- Call Ollama's /api/chat as described in docs/ollama-chat-notes.md, with "stream": false.
- Use requests; add it to requirements.txt if it isn't there yet. No other new dependencies.
- Don't change /health, /echo, or /models.
- The server doesn't store the conversation. The client sends the full history each time.
- Use a finite timeout for the Ollama request.

## Out of scope
Streaming replies, saving conversations, a web page for chatting.

## Done when
- In /docs, send a user message and confirm a 200 response with reply and model, using the default model when omitted.
- Send a multi-message history and confirm the reply remembers the earlier name.
- Send an empty messages list and a request without messages; both return 422.
- Request an unavailable model and confirm 502 includes Ollama's error message.
- Stop Ollama and confirm the same valid request returns the specified 503 message.
- Confirm /health, /echo, and /models retain their existing behavior.
