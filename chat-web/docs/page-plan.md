1. **Serve the page and local assets.** Update `main.py` to serve `static/index.html` at `/` and files under `/static`. Create the three specified files in `static/`.  
   **Check:** Start the app with `uvicorn main:app --reload`; open `/` and confirm it loads. Visit `/docs` and confirm `/health`, `/echo`, `/models`, and `/chat` are still listed.

2. **Add the page structure.** In `static/index.html`, add a labeled model selector, conversation area, labeled message input, Send button, New chat button, and an area for status and errors. Link the local CSS and JavaScript files.  
   **Check:** Reload `/` and confirm every control is visible and has a clear label. Tab through the controls using only the keyboard.

3. **Make the page readable.** In `static/style.css`, add simple spacing, readable message styling, visible keyboard focus, and a layout that works at narrow widths.  
   **Check:** Resize the browser and confirm controls and messages remain readable and usable without horizontal scrolling.

4. **Load installed models.** In `static/app.js`, request `GET /models` and populate the selector with the returned names. Show a readable message if models cannot be loaded or none are available.  
   **Check:** With Ollama running, compare the selector with `/models`. Stop Ollama, reload the page, and confirm a readable error appears.

5. **Send and display a conversation.** In `static/app.js`, keep conversation history in a JavaScript list, display the submitted message immediately, and send the selected model and full history to `POST /chat`. Display the reply and add both messages to history after success. Use `textContent` for message text.  
   **Check:** With Ollama running, send a message using the button and confirm it appears before the reply. Send text containing `<i>hi</i>` and confirm the tags appear literally.

6. **Add keyboard submission and request feedback.** In `static/app.js`, make Enter send and Shift+Enter insert a newline. While a reply is pending, show an in-progress status and prevent another send.  
   **Check:** Send with Enter, then verify Shift+Enter adds a newline without sending. During a request, confirm the status is visible and repeated button presses or Enter cannot send again.

7. **Handle failed requests and recovery.** In `static/app.js`, show the `/chat` error’s `detail` in plain language, remove the failed message from the conversation and history, and restore the controls after the request ends.  
   **Check:** Stop Ollama and send a message; confirm a readable error appears and the failed message is absent. Restart Ollama and confirm a new message sends successfully.

8. **Add New chat.** In `static/app.js`, clear both the displayed conversation and its in-memory history when New chat is activated. Ensure a pending reply cannot repopulate a newly cleared chat.  
   **Check:** Tell the model a name and ask a follow-up to verify it has context. Start a new chat, ask the follow-up again, and confirm the earlier messages are gone and are not sent in the new request.

9. **Run the full acceptance check.** Review `main.py` and the three `static/` files against [page-spec.md](/Users/koloma/agentic-ai/chat-web/docs/page-spec.md).  
   **Check:** Repeat the keyboard-only flow, successful and stopped-Ollama checks, and confirm `/docs` and the existing routes still work. Verify all assets are local, no dependencies were added, and the existing route behavior was not changed.