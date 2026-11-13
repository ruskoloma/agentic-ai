# Spec: the chat page

## Goal
Give someone using this local app a simple page to choose an installed model and have a conversation with it. Keep the interaction readable and easy to restart.

## What the user can do
- Open http://127.0.0.1:8000/ and see the chat page.
- Pick a model from a list of installed models (from GET /models).
- Type a message and send it with the Send button or the Enter key (Shift+Enter makes a new line).
- See their message, then the model's reply.
- Keep chatting: the page remembers the conversation and sends the whole history to POST /chat each time.
- Start over with a New chat button that clears the conversation.

## Behavior details
- While waiting for a reply, the Send button is disabled and the page shows that it's working.
- If /chat returns an error (for example 503 when Ollama is quit), show the error's message on the page in plain words. The failed message is not added to the conversation.
- All message text is shown as plain text: a message like <i>hi</i> appears with the tags visible.

## Constraints
- Files: static/index.html, static/style.css, static/app.js. Serve the page at GET / and the files under /static.
- Plain HTML, CSS, and JavaScript. No frameworks, no build step, nothing loaded from other websites.
- No new Python dependencies. Don't change /health, /echo, /models, or /chat.
- The conversation lives in the browser (a JavaScript list). The server still stores nothing.
- Make all controls usable with a keyboard and provide labels for the message and model inputs.

## Out of scope
Keeping conversations after a page reload, streaming replies, user accounts, styling beyond clean and readable.

## Done when
- Opening the root shows the page; /docs still lists all four existing routes.
- The model selector shows the installed model names returned by /models.
- A message sent by button and one sent by Enter each appear before their replies; Shift+Enter inserts a newline without sending.
- After telling the model a name, a follow-up question gets an answer using the earlier message.
- New chat clears the visible conversation and its memory; a subsequent question no longer has the earlier context.
- During a request, an in-progress indication appears and a second send cannot be triggered.
- With Ollama stopped, a readable error appears, the failed message is excluded from conversation history, and sending works after restart.
- Messages containing HTML-like tags display those characters literally.
- Labels and keyboard navigation let someone select a model, type, send, and clear without a mouse.
- Assets are local plain HTML, CSS, and JavaScript, and no extra Python dependency or change to existing routes is introduced.
