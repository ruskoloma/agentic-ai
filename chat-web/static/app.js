const model = document.querySelector('#model');
const reloadModels = document.querySelector('#reload-models');
const newChat = document.querySelector('#new-chat');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const send = document.querySelector('#send');
let history = [];
let busy = false;

function updateControls() {
  send.disabled = busy || model.disabled || !model.value;
  newChat.disabled = busy;
  reloadModels.disabled = busy;
  input.disabled = busy;
  model.disabled = busy || model.options.length === 0;
}

async function loadModels() {
  model.disabled = true;
  send.disabled = true;
  reloadModels.disabled = true;
  status.textContent = 'Loading models…';
  try {
    const response = await fetch('/models');
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Could not load models.');
    model.replaceChildren();
    for (const name of data.models) {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      model.append(option);
    }
    status.textContent = data.models.length ? '' : 'No models are installed. Refresh after installing one.';
  } catch (error) {
    model.replaceChildren();
    status.textContent = error.message || 'Could not load models. Please try again.';
  }
  model.disabled = model.options.length === 0;
  updateControls();
}

function showMessage(role, content) {
  const item = document.createElement('div');
  item.className = 'message';
  const label = document.createElement('strong');
  label.textContent = role === 'user' ? 'You' : 'Model';
  const text = document.createElement('p');
  text.textContent = content;
  item.append(label, text);
  messages.append(item);
  item.scrollIntoView({ block: 'nearest' });
  return item;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const content = input.value.trim();
  if (busy || model.disabled || !model.value || !content) return;
  const userMessage = { role: 'user', content };
  const displayedMessage = showMessage('user', content);
  busy = true;
  updateControls();
  status.textContent = 'Waiting for a reply…';
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: model.value, messages: [...history, userMessage] })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Could not send the message.');
    history.push(userMessage, { role: 'assistant', content: data.reply });
    showMessage('assistant', data.reply);
    input.value = '';
    status.textContent = '';
  } catch (error) {
    displayedMessage.remove();
    status.textContent = error.message || 'Could not send the message. Please try again.';
  } finally {
    busy = false;
    model.disabled = model.options.length === 0;
    updateControls();
    input.focus();
  }
});

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    form.requestSubmit();
  }
});

newChat.addEventListener('click', () => {
  history = [];
  messages.replaceChildren();
  input.value = '';
  status.textContent = '';
  input.focus();
});

loadModels();
