# VS Code AI session log

## 2026-11-03 — Project review with Codex
- First prompt: “What files and folders are in this project, and what is each one for? Don't change any files.”
- Follow-ups: Review the health and echo routes against their requirements, then explain why an empty object produces a 422 response.
- Turns: 3 · New thread: yes.
- Codex inspected the project files and described the routes and validation. No approval prompt was observed.

## 2026-11-03 — Project rules memory check with Codex
- Prompt in each of two new threads: “How do I run this project, and what rules should you follow when you change it? Don't change any files.”
- Turns: 1 per thread. No approval prompt was observed.
- Before AGENTS.md existed, Codex identified the run command from the README. Afterward, it listed the run command and project rules, including asking before adding dependencies.

## 2026-11-03 — GET /models with Codex
- First prompt: “Goal: Add GET /models to main.py, returning {\"models\": [\"model-name\", ...]} using model names from http://localhost:11434/api/tags.
  Constraints: Keep /health and /echo unchanged. Use Python’s built-in urllib and json, with a timeout; do not add dependencies. Return HTTP 503 with a clear message if Ollama is unavailable. Do not run the server or tests; I will check them.
  Done when: With Ollama running, /models lists the installed names, and with Ollama stopped it returns 503 instead of crashing.”
- Turns: 1 · New thread: yes. No command approval was requested.
- Codex edited main.py and reported using urllib and json with no new dependency.
