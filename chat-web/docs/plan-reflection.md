# One-shot and planned page comparison

| Measure | One-shot | Planned |
|---|---|---|
| Chats used | 1 | 6: planning and five implementation steps |
| My messages across those chats | 1 | 8: the planning prompt, five step prompts, and two corrections |
| Implementation files changed | 4: `main.py` and three static assets | 4: `main.py` and three static assets; the branch also records the plan |
| Page checks passed | 8 of 8 in the browser checks | 8 of 8 after the step 4 correction |
| Problems found | None of the eight checks failed. New chat is disabled while waiting for a reply. | Step 1 initially named the JavaScript file `script.js`; I requested the specified `app.js`. The step 3 result waited for the reply before displaying the user's message; I requested a correction in step 4. |
| Rough time | About 3 minutes for the build, plus manual testing | About 12 minutes for planning and the five agent chats, plus review, commits, and manual testing |

Planning made the work easier to inspect: each step had a check and its own commit, such as step 4's `chat-web: step 4, keyboard and error recovery`. The checks exposed a wrong asset filename and a delayed message display, which were corrected before finishing. The one-shot build passed the same eight checks without those corrections, so planning did not produce a clear advantage in the number of checks passed here; it cost extra chats and review time. I selected the planned version because its incremental history is easier to review and it allows New chat during a pending reply while ignoring the old response. For a small, easily reviewed change I would use a single prompt and check the result; for a feature with several interacting behaviors and failure cases, I would write and review a plan first.
