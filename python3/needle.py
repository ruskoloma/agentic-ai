"""Measure when the model stops recalling a fact at the start of a long prompt."""

import requests

MODEL = "llama3.2:3b"
URL = "http://localhost:11434/api/generate"
NEEDLE = "The maintenance code is ZEBRA-42."
SIZES = [200, 800, 2000, 5000, 10000]


def build_prompt(filler_words):
    """Put the fact first, the requested filler in the middle, and the question last."""
    sentence = "The quarterly report was filed on time and contained no surprises."
    filler = " ".join((sentence * (filler_words // 11 + 1)).split()[:filler_words])
    return (
        f"IMPORTANT FACT: {NEEDLE}\n\n{filler}\n\n"
        "Question: What was the IMPORTANT FACT stated at the very beginning? "
        "Answer with the fact only."
    )


def ask(prompt):
    """Send one prompt to Ollama and return the answer and prompt token count."""
    response = requests.post(
        URL,
        # Raising num_ctx to 16384 moves the limit beyond Ollama's default context window.
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 16384},
        },
        timeout=900,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"], data.get("prompt_eval_count", 0)


def main():
    """Test increasingly long prompts and stop at the first missed fact."""
    try:
        for size in SIZES:
            answer, tokens = ask(build_prompt(size))
            recalled = NEEDLE in answer
            print(f"{size:>6,} filler words  {tokens:>6,} tokens  recalled: {recalled}")
            if not recalled:
                print(f"recall failed at {size} filler words (~{tokens} tokens)")
                break
    except requests.ConnectionError:
        print("Can't reach Ollama - is it running?")


if __name__ == "__main__":
    main()
