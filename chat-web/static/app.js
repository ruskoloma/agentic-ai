const model = document.querySelector('#model');
const message = document.querySelector('#message');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
const send = document.querySelector('#send');
const newChat = document.querySelector('#new-chat');
const chatHistory = [];
let pending = false;
let conversationVersion = 0;

function setPending(value) {
  pending = value;
  send.disabled = value;
  message.disabled = value;
  model.disabled = value;
}

function resetChat() {
  conversationVersion++;
  chatHistory.length = 0;
  messages.replaceChildren();
  message.value = '';
  status.textContent = '';
  setPending(false);
}

async function loadModels() {
  try {
    const response = await fetch('/models');
    if (!response.ok) throw new Error('Could not load models.');
    const data = await response.json();
    if (!Array.isArray(data.models) || !data.models.every(name => typeof name === 'string')) {
      throw new Error('Could not load models.');
    }
    if (data.models.length === 0) {
      status.textContent = 'No models available in Ollama.';
      return;
    }
    for (const name of data.models) {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      model.append(option);
    }
  } catch (error) {
    status.textContent = 'Could not load models. Check that Ollama is running and reload the page.';
  }
}

function showMessage(role, content) {
  const line = document.createElement('p');
  line.textContent = `${role}: ${content}`;
  messages.append(line);
  return line;
}

async function sendMessage() {
  if (pending) return;
  const content = message.value.trim();
  if (!model.value || !content) {
    status.textContent = 'Select a model and enter a message.';
    return;
  }

  const userMessage = { role: 'user', content };
  const requestVersion = conversationVersion;
  setPending(true);
  status.textContent = 'Waiting for a reply...';
  const userLine = showMessage('You', content);
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: model.value, messages: [...chatHistory, userMessage] }),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(typeof data.detail === 'string' ? data.detail : 'Could not get a reply. Please try again.');
    }
    const data = await response.json();
    if (requestVersion !== conversationVersion) return;
    if (typeof data.reply !== 'string') throw new Error('Invalid reply.');
    chatHistory.push(userMessage, { role: 'assistant', content: data.reply });
    showMessage('Model', data.reply);
    message.value = '';
    status.textContent = '';
  } catch (error) {
    if (requestVersion !== conversationVersion) return;
    userLine.remove();
    status.textContent = error.message || 'Could not get a reply. Please try again.';
  } finally {
    if (requestVersion === conversationVersion) setPending(false);
  }
}

send.addEventListener('click', sendMessage);
newChat.addEventListener('click', resetChat);
message.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    sendMessage();
  }
});

loadModels();
