# Vercel Event Calendar (Demo)

This repository is a Vercel-compatible demo of an MCP-based Event Calendar server.

- API endpoint: `/api/mcp`
- Frontend: `public/index.html` (simple chat UI)

Quick local test

1. Install dev deps for local testing:

```bash
python -m pip install -r requirements.txt
```

2. Run the test harness:

```bash
python test_local.py
```

Deploy to Vercel

1. Ensure `vercel` CLI is installed and logged in.
2. Run `vercel deploy` and follow prompts.
3. Your serverless endpoint will be available at `https://<project>.vercel.app/api/mcp`.

Notes

- Vercel serverless functions are stateless — events are stored in-memory and **will reset** frequently.
- The demo includes a **conversational** `handle_message` tool that accepts both terse commands and natural language. Examples:
  - `list` or `list events` → lists all events
  - `list events on 2026-01-01` or `What's on 2026-01-01?` → lists events for that date
  - `summarize` / `summary` / `what's coming up` → summary of upcoming events
  - `add:Title|YYYY-MM-DD|Desc` (shorthand, still supported)
  - `Add Birthday on 2026-02-01 about cake` → conversational add
  - `Create Meeting on 2026-03-03` → conversational add
  - `Add Meeting tomorrow` → supports `today` and `tomorrow`
  - `delete:Title` or `delete Meeting` or `remove Meeting` → deletes by title

  If a message isn't understood, the handler returns a short help text with examples.

Frontend improvements:

- Chat UI now supports typing indicator, timestamps, avatars, copy-to-clipboard buttons, Shift+Enter for newlines, Enter to send, and conversation persistence in `localStorage`. The composer shows a spinner while the backend responds and disables input until a reply is received.

## Development & Contributing

If you plan to edit or extend this project, see `DEVELOPING.md` for a detailed developer guide (setup, editing the frontend and backend, testing, and deployment to Vercel).

Contributions should follow the branch-per-feature workflow and include clear commit messages (use prefixes like `feat:`, `fix:`, `style:`, or `docs:`). Please open a PR for review and testing before merging to the main branch.
