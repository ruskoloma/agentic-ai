# Test plan

| # | Behavior (from my specs) | What it checks (my words) | Test name |
|---|---|---|---|
| 1 | GET /health returns {"status": "ok"} | The health endpoint reports the exact healthy response. | `test_health_returns_ok` |
| 2 | POST /echo returns the message and its length | The endpoint returns the submitted text and its correct character count. | `test_echo_returns_message_and_character_count` |
| 3 | POST /echo with no message is 422 | Missing message input produces a useful validation error. | `test_echo_without_message_returns_validation_error` |
| 4 | GET /models lists installed model names | Model names returned by Ollama appear in the response. | `test_models_lists_installed_names` |
| 5 | GET /models is 503 when Ollama is down | A connection failure returns service unavailable and an explanation. | `test_models_returns_503_when_ollama_is_down` |
| 6 | POST /chat returns the reply and the model used | A successful chat returns the assistant's text and selected model. | `test_chat_returns_reply_and_default_model` |
| 7 | POST /chat sends the whole history to Ollama, with "stream": false | The outgoing request preserves every message in order and disables streaming. | `test_chat_sends_whole_history_without_streaming` |
| 8 | POST /chat uses the model I pick | The outgoing request uses the model supplied by the caller. | `test_chat_uses_selected_model` |
| 9 | POST /chat with an empty history is 422 | An empty message list is rejected with a validation error. | `test_chat_rejects_empty_or_missing_history` |
| 10 | POST /chat is 502 with Ollama's message when Ollama answers with an error | An upstream error becomes a bad gateway response including its explanation. | `test_chat_returns_502_with_ollama_error` |
| 11 | POST /chat is 503 when Ollama is down | A connection failure yields service unavailable and a useful explanation. | `test_chat_returns_503_when_ollama_is_down` |
| 12 | GET / serves the chat page with its controls | The root serves HTML containing the controls needed to use chat. | `test_root_serves_chat_page_with_controls` |
