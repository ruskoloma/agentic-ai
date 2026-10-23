# Model Autopsy

I tested `llama3.2:3b` locally through Ollama on October 22, 2026. These are the exact prompts and short answers I received. I checked each answer against primary documentation or a direct Python check.

## 1. Invented Laravel helper

**Prompt:** In one sentence, what does Laravel's `Str::obfuscate()` do?

**Model answer:**

> Laravel's Str::obfuscate() method replaces all non-alphanumeric characters in a string with an asterisk (*), effectively obfuscating or hiding sensitive information, such as passwords or credit card numbers.

**How I checked:** I searched the [Laravel framework's `Str.php` source](https://github.com/laravel/framework/blob/13.x/src/Illuminate/Support/Str.php) for `obfuscate`; it has no match. The source does define `Str::mask()`, and [Laravel's string documentation](https://laravel.com/framework/docs/strings) describes that real method as masking a portion of a string. The model invented both the helper and its behavior.

## 2. Invented pathlib method

**Prompt:** In one sentence, what does `pathlib.Path.read_json()` do?

**Model answer:**

> pathlib.Path.read_json() reads the contents of a JSON file located at the specified path and returns a Python dictionary representing the JSON data.

**How I checked:** I ran this in the course virtual environment:

```text
$ python -c 'from pathlib import Path; print(hasattr(Path, "read_json"))'
False
```

The [official pathlib documentation](https://docs.python.org/3/library/pathlib.html) lists the `Path` file-reading methods and has no `read_json()` method. The method and its claimed return value were fabricated.

## 3. Outdated current-version answer

**Prompt:** What is the newest version of Python?

**Model answer:**

> The newest version of Python is Python 3.10, which was released on September 27, 2021.

**How I checked:** I checked the [official Python release page for 3.15.1](https://www.python.org/downloads/release/python-3151/). It identifies Python 3.15.1 as a release dated October 21, 2026, one day before I checked. The model gave a release from 2021 as current.

## Context-window measurements

- With Ollama's default context, recall first failed at **5,000 filler words**; Ollama reported **about 2,050 prompt tokens**.
- With `num_ctx=16384`, recall still worked at **10,000 filler words** (**10,068 prompt tokens**). Following the lab's extended check, it failed at **20,000 filler words**; Ollama reported **8,194 prompt tokens** for that request.
