import io
import json
from html.parser import HTMLParser
from types import SimpleNamespace
from unittest.mock import Mock
from urllib.error import URLError

import pytest
import requests
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def ollama(monkeypatch):
    # Unexpected Ollama calls fail before any network request can be made.
    post = Mock(side_effect=AssertionError("Unexpected Ollama chat call"))
    urlopen = Mock(side_effect=AssertionError("Unexpected Ollama models call"))
    monkeypatch.setattr(main.requests, "post", post)
    monkeypatch.setattr(main, "urlopen", urlopen)
    return SimpleNamespace(post=post, urlopen=urlopen)


@pytest.fixture
def client(ollama):
    with TestClient(main.app) as test_client:
        yield test_client


def allow_chat(ollama, reply="Hello!"):
    ollama.post.side_effect = None
    ollama.post.return_value = Mock(
        ok=True, json=Mock(return_value={"message": {"content": reply}})
    )


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo_returns_message_and_character_count(client):
    message = "Hello, café 👋"

    response = client.post("/echo", json={"message": message})

    assert response.status_code == 200
    assert response.json() == {"message": message, "length": len(message)}


def test_echo_without_message_returns_validation_error(client):
    response = client.post("/echo", json={})

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "message"]
        and "required" in error["msg"].lower()
        for error in errors
    )


def test_models_lists_installed_names(client, ollama):
    ollama.urlopen.side_effect = None
    ollama.urlopen.return_value = io.BytesIO(
        json.dumps(
            {"models": [{"name": "llama3.2:3b"}, {"name": "qwen2.5:7b"}]}
        ).encode()
    )

    response = client.get("/models")

    assert response.status_code == 200
    assert response.json() == {"models": ["llama3.2:3b", "qwen2.5:7b"]}
    ollama.urlopen.assert_called_once_with(
        "http://localhost:11434/api/tags", timeout=5
    )


def test_models_returns_503_when_ollama_is_down(client, ollama):
    ollama.urlopen.side_effect = URLError("Connection refused")

    response = client.get("/models")

    assert response.status_code == 503
    assert response.json() == {
        "detail": (
            "Ollama is unavailable or returned an invalid response. "
            "Ensure Ollama is running."
        )
    }
    ollama.urlopen.assert_called_once()


def test_chat_returns_reply_and_default_model(client, ollama):
    allow_chat(ollama, reply="Hello, Ada!")

    response = client.post(
        "/chat", json={"messages": [{"role": "user", "content": "I'm Ada."}]}
    )

    assert response.status_code == 200
    assert response.json() == {"reply": "Hello, Ada!", "model": "llama3.2:3b"}
    assert ollama.post.call_args.kwargs["json"]["model"] == "llama3.2:3b"


def test_chat_sends_whole_history_without_streaming(client, ollama):
    allow_chat(ollama, reply="Your name is Ada.")
    messages = [
        {"role": "system", "content": "Remember the user's name."},
        {"role": "user", "content": "I'm Ada."},
        {"role": "assistant", "content": "Hello, Ada!"},
        {"role": "user", "content": "What is my name?"},
    ]

    response = client.post("/chat", json={"messages": messages})

    assert response.status_code == 200
    assert response.json() == {
        "reply": "Your name is Ada.",
        "model": "llama3.2:3b",
    }
    ollama.post.assert_called_once_with(
        "http://localhost:11434/api/chat",
        json={"model": "llama3.2:3b", "messages": messages, "stream": False},
        timeout=60,
    )


def test_chat_uses_selected_model(client, ollama):
    allow_chat(ollama)
    messages = [{"role": "user", "content": "Hi"}]

    response = client.post(
        "/chat", json={"messages": messages, "model": "qwen2.5:7b"}
    )

    assert response.status_code == 200
    assert response.json() == {"reply": "Hello!", "model": "qwen2.5:7b"}
    ollama.post.assert_called_once_with(
        "http://localhost:11434/api/chat",
        json={"model": "qwen2.5:7b", "messages": messages, "stream": False},
        timeout=60,
    )


@pytest.mark.parametrize("payload", [{"messages": []}, {}], ids=["empty", "missing"])
def test_chat_rejects_empty_or_missing_history(client, ollama, payload):
    response = client.post("/chat", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "messages"] and error["msg"]
        for error in errors
    )
    ollama.post.assert_not_called()


def test_chat_returns_502_with_ollama_error(client, ollama):
    ollama.post.side_effect = None
    ollama.post.return_value = Mock(
        ok=False, json=Mock(return_value={"error": "model 'missing' not found"})
    )

    response = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Hi"}], "model": "missing"},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "Ollama error: model 'missing' not found"}
    ollama.post.assert_called_once()


def test_chat_returns_503_when_ollama_is_down(client, ollama):
    ollama.post.side_effect = requests.ConnectionError("Connection refused")

    response = client.post(
        "/chat", json={"messages": [{"role": "user", "content": "Hi"}]}
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Can't reach Ollama. Is it running?"}
    ollama.post.assert_called_once()


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = {}
        self.labels = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.elements[attrs["id"]] = (tag, attrs)
        if tag == "label":
            self.labels.add(attrs.get("for"))


def test_root_serves_chat_page_with_controls(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    page = PageParser()
    page.feed(response.text)
    for element_id, tag in {
        "model": "select",
        "message": "textarea",
        "send": "button",
        "new-chat": "button",
    }.items():
        assert page.elements[element_id][0] == tag
    assert {"messages", "status"} <= page.elements.keys()
    assert {"model", "message"} <= page.labels
    assert page.elements["status"][1]["role"] == "status"
    assert "Send" in response.text
    assert "New chat" in response.text
