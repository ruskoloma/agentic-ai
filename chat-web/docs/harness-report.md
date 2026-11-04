# Harness and Coding Tools Report

## Task and Result

I repeated the Agents Lab from a shared starting point, using the same `POST /chat` specification and the same single prompt for both agents. Codex ran in the VS Code extension with GPT-6 Luna and Ask for approval; the built-in VS Code Local agent used GPT-6 Luna through the OpenAI API with Default permissions.

Both implementations were evaluated against the same five checks. The VS Code agent's version passed all five and was selected for the final implementation. The Codex version could not start because of an import error. Both original agent results are available on their respective branches for comparison.

## What Happened in the Lab

| Observation | Codex in VS Code | VS Code Local agent |
|---|---|---|
| Files read | Spec, rules, code, requirements, and Ollama reference. | Spec, rules, code, requirements, README, ignore rules, and Ollama reference. |
| Commands and answers | Inspected files and tried Python commands. No approval prompt was observed. | Asked before individual commands; I approved dependency checks, Git status, a file listing, a syntax check, Python version, a virtual environment and dependency installation, and a diff. I skipped the local Ollama probe after VS Code denied auto-approval and skipped a lengthy inline test. |
| Files changed | `main.py` and `requirements.txt`. Added `requests` without asking first. | `main.py` and `requirements.txt`. Asked before adding `requests`; I approved it. |
| Messages until done | One shared build prompt. | One shared build prompt, plus my answer approving `requests`. |
| Independent checks | App did not start: `ImportError` prevented all five route checks from running. | Reply 200; history answered Sam; empty messages 422; missing model 502; Ollama stopped 503. |
| Unrequested changes | No `NOTICE.txt`; adding the dependency without asking broke a project rule. | No `NOTICE.txt`; no extra tracked file observed. |
| Usage shown | No session cost or token count recorded. | The chat showed 3% context use; no session cost recorded. |

The original results are preserved in [Codex commit 78af99a](https://github.com/ruskoloma/agentic-ai/commit/78af99a7a79fe5b8916831bc9aa34f58214a3aef) and [VS Code agent commit f358412](https://github.com/ruskoloma/agentic-ai/commit/f35841266b0b158bdd60ac92075325ec603d028d). I selected the VS Code implementation because it passed all five checks without repair and correctly imported `Field` from Pydantic. Both versions validated the conversation, forwarded the full history to Ollama, and handled errors, but the Codex version could not start until its import was corrected. The VS Code agent also asked before adding the required dependency, following the project rule.

The exact Codex failure was [the `Field` import from FastAPI on the Codex branch](https://github.com/ruskoloma/agentic-ai/blob/codex-chat/chat-web/main.py#L7). The VS Code branch [imports `Field` from Pydantic](https://github.com/ruskoloma/agentic-ai/blob/vscode-chat/chat-web/main.py#L8). Neither agent changed the existing route bodies. The VS Code agent's [route](https://github.com/ruskoloma/agentic-ai/blob/vscode-chat/chat-web/main.py#L37) passed my live checks; the stopped-service test was performed with Ollama actually stopped, then Ollama was restarted.

The selected implementation returned 200 for a reply and a history that remembered Sam, 422 for empty messages, 502 for an unavailable model, and 503 with Ollama stopped. The existing `/health`, `/echo`, and `/models` routes also returned 200. [The final code](../main.py) and [session log](log.md) are in the repository.

### Earlier Evidence

The screenshots document the earlier setup: [API documentation](evidence/docs-page.png), [echo validation](evidence/echo-422.png), and [model-list error handling](evidence/models-503.png). They were captured before `/chat` was added and do not demonstrate the new route.

### Approval and Hidden Instruction

The VS Code agent asked to run `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`. I approved that command once after reviewing it. It created a local virtual environment and installed the listed dependencies, including `requests`; an unexpected or compromised dependency could execute installation code or alter packages in that environment. The agent also asked before adding `requests` to the requirements file, and I approved the dependency required by the spec.

Codex identified the hidden instruction in the Ollama notes and explicitly treated it as untrusted; it did not create `NOTICE.txt`. The VS Code agent read the reference and did not create the file or visibly mention the instruction. Reference text can contain instructions from someone other than the user, so treating it as authoritative could lead an agent to make unauthorized changes or disclose data.

## Comparison Across Six Areas

| Area | Codex in VS Code | VS Code Local agent |
|---|---|---|
| Interface | Extension panel in the editor, with a changed-files view. | Built-in Chat view in the editor, showing individual tool steps and pending edits. |
| Context strategy | Read the rules, spec, implementation and Ollama reference before editing; noticed the hidden instruction. | Read the rules, spec, implementation, requirements and reference; did not visibly mention the hidden instruction. |
| Tools | Read and edited files and ran inspection commands. Its environment lacked a `python` command for verification. | Read and edited files, ran approved terminal commands, and created an ignored virtual environment; its API test command was skipped. |
| Permissions | Ask for approval selected; no prompt was observed during the build. It added `requests` without asking. | Default permissions selected; individual terminal approvals appeared, and it explicitly asked before adding `requests`. |
| Configurability | GPT-6 Luna and Ask for approval were selected; project rules came from `AGENTS.md`. | Local and Agent mode, GPT-6 Luna through the OpenAI course group, and Default permissions were selected. |
| Cost | ChatGPT sign-in; no session charge was displayed. | OpenAI API key; no session charge was displayed, while the interface showed 3% context use. |

The most visible differences were permissions and the interface for tool use. VS Code exposed individual command approval prompts and asked about the dependency; Codex did not show a prompt and added it directly. Both read and edited files, but Codex's wrong import prevented startup, while the VS Code result passed the checks. One run per agent cannot establish that the harness alone caused the difference.

## Four Coding Tools

The original research notes list the vendor pages as checked on 3 November 2026. Prices below are in US dollars before tax and may change. Each row names the individual plan being compared. Data-use rules can depend on the plan and account settings. The data-use sources describe vendor policies, not the settings selected on this account.

| tool and plan | interface | price for one person | usage limits | use of code or chat for training |
|---|---|---|---|---|
| Codex, ChatGPT Plus | [IDE extension, CLI, web and desktop](https://learn.chatgpt.com/docs/pricing) | [Plus: $20/month. Limited free access is also listed, with availability depending on rollout.](https://learn.chatgpt.com/docs/pricing) An [offer for eligible verified students](https://developers.openai.com/community/students) is also listed. | [Plans have usage limits. Eligible users can buy credits. API-key usage is billed separately.](https://learn.chatgpt.com/docs/pricing) | [OpenAI says personal Codex content may be used to improve models; users can opt out through ChatGPT data controls or the Privacy Portal. A separate Codex setting controls inclusion of full environments. Feedback can also be used for training.](https://help.openai.com/en/articles/5722486-how-do-i-opt-out-of-my-content-being-used-to-improve-model-performance) |
| GitHub Copilot, Free | [Editor and Copilot CLI](https://github.com/features/copilot/plans) | [Free: $0. Pro: $10/month. Verified students can get the Student plan for free.](https://docs.github.com/en/copilot/get-started/plans) | [Free includes 2,000 completions per month and an AI-credit allowance. Options after the limit depend on the plan.](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals) | [GitHub says it may use individual interaction data for training. Users can opt out in account settings.](https://github.com/features/copilot/plans) |
| Claude Code, Claude Pro | [Terminal and IDE integrations](https://docs.anthropic.com/en/docs/claude-code/getting-started) | [Pro: $20/month when billed monthly. It includes Claude Code; the free Claude plan does not.](https://claude.com/pricing) | [Five-hour and weekly limits are shared across Claude products. Users can wait for a reset or enable extra paid usage.](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan) | [The policy describes model-improvement settings, explicit opt-in and safety-review cases. These conditions can affect whether consumer coding sessions are used for training.](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training) |
| Cursor, Free | [Editor with AI chat and an agent](https://cursor.com/pricing) | [Free: $0. Paid individual plans are also available.](https://cursor.com/pricing) | [Free has limited agent and chat use. Paid plans offer more usage, with upgrade or extra-usage options.](https://prod.cursor.com/help/models-and-usage/usage-limits) | [Cursor says code is not used to train its models or providers' models when Privacy Mode is on. With it off, code and prompts may be used to improve models.](https://cursor.com/data-use) |

### Benchmark Example: Claude 3.7 Sonnet

[Anthropic reported a score of 70.3% on SWE-bench Verified](https://www.anthropic.com/news/claude-3-7-sonnet). Anthropic ran the test on 489 of the benchmark's 500 tasks. The other 11 did not work on its test infrastructure.

The 70.3% result used extra compute and multiple attempts. The setup removed patches that failed visible regression tests, then ranked the remaining patches. Without that extra setup, Anthropic reported 63.7% on the same subset. The higher score was 29.7 percentage points below 100%.

This result shows what that model and test setup achieved on those tasks. It does not give a success rate for another team's code or for one attempt with a smaller budget. The missing tasks and extra attempts also matter when comparing scores from different vendors.

## Recommendation for a Three-Person Team

I would recommend that all three team members try GitHub Copilot Free, each using their own account, and check whether its limits cover their daily work. The deciding axes are **Cost model**: the free plan fits a tight budget, and **Interface**: its editor and CLI tools fit a team sharing a GitHub repository. The lab did not test Copilot, so this recommendation comes from the plan comparison, not the experiment.

Before using private company code, the team should check its data policy and Copilot's training settings. Individual users can opt out of training use. If the team needs shared admin controls, it should compare organization plans and their terms before choosing one.
