# Test plan

| # | Behavior (from my specs) | What it checks (my words) | Test name |
|---|---|---|---|
| 1 | GET /health returns {"status": "ok"} | The health endpoint reports the exact healthy response. | |
| 2 | POST /echo returns the message and its length | The endpoint returns the submitted text and its correct character count. | |
| 3 | POST /echo with no message is 422 | Missing message input produces a useful validation error. | |
| 4 | GET /models lists installed model names | Model names returned by Ollama appear in the response. | |
| 5 | GET /models is 503 when Ollama is down | A connection failure returns service unavailable and an explanation. | |
| 6 | POST /chat returns the reply and the model used | A successful chat returns the assistant's text and selected model. | |
| 7 | POST /chat sends the whole history to Ollama, with "stream": false | The outgoing request preserves every message in order and disables streaming. | |
| 8 | POST /chat uses the model I pick | The outgoing request uses the model supplied by the caller. | |
| 9 | POST /chat with an empty history is 422 | An empty message list is rejected with a validation error. | |
| 10 | POST /chat is 502 with Ollama's message when Ollama answers with an error | An upstream error becomes a bad gateway response including its explanation. | |
| 11 | POST /chat is 503 when Ollama is down | A connection failure yields service unavailable and a useful explanation. | |
| 12 | GET / serves the chat page with its controls | The root serves HTML containing the controls needed to use chat. | |
