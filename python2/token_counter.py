"""token_counter.py — Python II assignment.

Report file sizes and token estimates, and count repeated words.
Run from the folder that contains sample.txt, hello.py, and token_tally.py.
"""

FILES = ["sample.txt", "hello.py", "token_tally.py"]


def estimate_tokens(words):
    return words * 4 // 3


def file_stats(path):
    with open(path, encoding="utf-8") as file:
        text = file.read()
    return len(text.splitlines()), len(text.split()), len(text)


def word_counts(path):
    counts = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            for word in line.split():
                cleaned_word = word.lower().strip(".,;:!?\"'()")
                if cleaned_word:
                    counts[cleaned_word] = counts.get(cleaned_word, 0) + 1
    return counts


def main():
    report_lines = [f"{'file':<18} {'lines':>5} {'words':>6} {'chars':>6} {'tokens':>7}"]
    total_tokens = 0

    for path in FILES:
        lines, words, characters = file_stats(path)
        tokens = estimate_tokens(words)
        total_tokens += tokens
        report_lines.append(
            f"{path:<18} {lines:>5} {words:>6} {characters:>6} {tokens:>7}"
        )

    report_lines.append(f"{'TOTAL':<18} {'':>5} {'':>6} {'':>6} {total_tokens:>7,}")
    for report_line in report_lines:
        print(report_line)

    counts = word_counts("sample.txt")
    repeated_words = sorted(
        (word, count) for word, count in counts.items() if count > 1
    )
    print("\nmost common words in sample.txt")
    for word, count in repeated_words:
        print(f"{word:<15} {count}")
    print(
        f"\n{len(counts)} different words; "
        f"{len(repeated_words)} of them appear more than once"
    )

    with open("report.txt", "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    main()
