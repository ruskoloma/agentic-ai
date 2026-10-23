"""token_tally.py — Python I assignment."""


def main():
    # PART A — words to tokens
    print("PART A — words to tokens")
    print(f"{'words':>7} {'tokens':>7}")
    for words in range(100, 1001, 100):
        tokens = words * 4 // 3
        print(f"{words:>7,} {tokens:>7,}")

    # PART B — the tier
    print("\nPART B — the tier")
    tier = "small"
    if tier == "small":
        speed = "fastest"
        limit = 4000
    elif tier == "mid":
        speed = "balanced"
        limit = 32000
    elif tier == "flagship":
        speed = "slowest"
        limit = 128000
    else:
        print(f"Unknown tier: {tier}")
        return

    print(f"tier   : {tier.upper()}")
    print(f"speed  : {speed}")
    print(f"limit  : {limit:,} tokens per conversation")

    # PART C — a 10-turn conversation
    print("\nPART C — a 10-turn conversation")
    turns = 10
    user_tokens = 200
    reply_tokens = 400
    history = 0
    print(f"{'turn':>4} {'sent':>7}")

    first_sent = None
    last_turn = None
    last_sent = None
    for turn in range(1, turns + 1):
        sent = history + user_tokens
        if first_sent is None:
            first_sent = sent
        flag = "  <-- over the limit" if sent > limit else ""
        print(f"{turn:>4} {sent:>7,}{flag}")
        last_turn = turn
        last_sent = sent
        if sent > limit:
            print(f"conversation stopped at turn {turn}")
            break
        # Add this turn and its reply after printing; both enter future history.
        history += user_tokens + reply_tokens

    print(f"Turn 1 sent {first_sent:,} tokens. Turn {last_turn} sent {last_sent:,} tokens.")
    print("Same message size every time — the history is what grew.")


if __name__ == "__main__":
    main()
