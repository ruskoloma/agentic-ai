"""A short conversation that re-sends the complete message history each turn."""

import requests

MODEL = "llama3.2:3b"
URL = "http://localhost:11434/api/chat"
PROMPTS = [
    "My name is Ruslan and my favorite language is Python. Remember that.",
    "In one sentence, what is a virtual environment?",
    "What is my name and my favorite language?",
]


def ask(history):
    """Send the conversation history and return the reply and prompt token count."""
    response = requests.post(
        URL,
        json={"model": MODEL, "messages": history, "stream": False},
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"], data.get("prompt_eval_count", 0)


def main():
    """Run the three assignment prompts as one remembered conversation."""
    history = []
    try:
        for turn, prompt in enumerate(PROMPTS, start=1):
            history.append({"role": "user", "content": prompt})
            reply, tokens = ask(history)
            history.append({"role": "assistant", "content": reply})
            print(f"--- turn {turn} ---")
            print(f"model: {reply.strip()}")
            print(f"[{len(history)} messages in history; {tokens} tokens sent this turn]")
    except requests.ConnectionError:
        print("Can't reach Ollama - is it running?")
        return

    # The token count climbs because the full conversation, including earlier replies, is sent again each turn.


if __name__ == "__main__":
    main()
