# Chat page implementation plan

- [x] Step 1: Serve a placeholder from `static/index.html` at `/`, mount `/static`, and create the three local assets. Check: start the app, open `/` and `/static/`, and confirm `/docs` lists all four existing routes.
- [x] Step 2: Add labeled model, conversation, message, send, new-chat and status controls; add readable responsive styling and keyboard focus. Check: open `/`, tab through controls, and resize the window.
- [x] Step 3: Load model names from `/models`, handle empty/error responses, and safely render a successful button-sent message and reply with browser-held history. Check: compare selector to `/models`, send `<i>hi</i>` and verify literal tags, then tell the model a name and ask it to recall it.
- [x] Step 4: Add Enter and Shift+Enter behavior, pending status and protection against duplicate sends, and recoverable `/chat` errors that leave failed messages out of history. Check: exercise both keys and busy state, stop Ollama for an error, restart and send successfully.
- [x] Step 5: Implement New chat with reset of displayed and in-memory history, including safe behavior during an outstanding request. Check: tell the model a name, reset, and verify the next exchange has no previous context; inspect `/docs` and verify local assets and unchanged dependencies and routes.

## Review notes

1. Combined the original structure and styling steps: both are limited to the same static interface and can be reviewed together, while the check explicitly covers keyboard access and narrow screens. Without a keyboard check the required labels might exist but still be unusable.
2. Moved the memory check into the successful send step. The original deferred this until reset; without an earlier multi-turn check, a history bug could be mistaken for a reset bug.
3. Grouped pending state with error recovery so controls are restored on both success and failure; treating these separately risks leaving the page disabled after an error. The check now explicitly stops and restarts Ollama.
4. Made clearing during an outstanding request an explicit reset check, avoiding a stale reply repopulating the new conversation. Kept checks of local assets and unchanged routes in the final step rather than a separate implementation chat.
