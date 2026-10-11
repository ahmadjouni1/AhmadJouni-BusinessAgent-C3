---
title: SunCedar Solar Concierge
emoji: ☀️
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.30.0
app_file: app.py
pinned: false
short_description: AI concierge for a fictional Lebanese solar company
---

# AhmadJouni-BusinessAgent-C3

AI concierge for SunCedar Solar, an LLM agent that answers questions, routes intents, captures leads, and logs feedback via tool calls. Built with Gemini + Gradio.

*EECE 503P/798S: Agentic Systems · C3: Introduction to Agents · Ahmad Jouni*

## What it is

**SunCedar Solar** is a fictional Lebanese company that installs home solar systems so families can stop depending on the
grid (EDL) and generator subscriptions. **Nour** is its virtual solar advisor. She:

- answers questions about packages, prices, warranty, payment and service areas, using **only** the business documents in `me/`
- **routes** every message to one of three paths: `general`, `lead`, or `feedback`
- **captures leads** (name, email, notes) with the `record_customer_interest` tool
- **logs feedback and unanswered questions** with the `record_feedback` tool
- **reflects** on each draft reply and revises it if it breaks the rules (bonus)
- replies in English, Arabic, or Arabizi, matching the user

## Architecture

```
user message
  │
  ├─► 1. ROUTER        LLM call → JSON {"intent": general|lead|feedback}; keyword fallback on failure
  │                    → picks a route hint + the tool set offered to the agent
  │
  ├─► 2. AGENT         system prompt (PERSONA + INSTRUCTIONS + summary.txt + PDF text) + route hint
  │                    + chat history (short-term memory) + tools
  │                    loop: model → tool calls? → execute → send results back → until final text
  │
  ├─► 3. TOOLS         record_customer_interest(email, name, message) → print + leads.jsonl
  │                    record_feedback(question)                      → print + feedback.jsonl
  │
  ├─► 4. REFLECTION    second LLM call checks the draft (invented info? missing email request?
  │                    false "recorded" claim? persona/language?) and revises → reflection.jsonl
  │
  └─► reply (Gradio ChatInterface shows router / tool / reflection steps as collapsible boxes)
```

| Route | Example | Handling |
|---|---|---|
| `general` | "What warranty do you give?" | Answer from docs; `record_feedback` available for unknowns |
| `lead` | "I want a quote for the Family package" | Collect name + email → `record_customer_interest` |
| `feedback` | "Do you install EV chargers?" / "Your installer was late" | `record_feedback`, thank, promise follow-up |

## Repository layout

```
├── me/
│   ├── about_business.pdf      # 6-page company profile (generated)
│   └── business_summary.txt    # short summary
├── business_agent.ipynb        # main deliverable: notebook, one section per assignment task
├── app.py                      # same logic, standalone (local + Hugging Face Spaces)
├── scripts/
│   ├── make_business_pdf.py    # regenerates me/about_business.pdf (reportlab)
│   └── build_notebook.py       # regenerates the notebook from app.py's sections
├── DEMO_SCRIPT.md              # test messages for the demo video
├── requirements.txt
├── .env.example                # copy to .env and add your key
└── .gitignore                  # ignores .env and the *.jsonl logs
```

`app.py` is the single source of truth for the logic. Its `# %% [section]` blocks are copied into the notebook by
`scripts/build_notebook.py`, so the notebook and the deployed app always run the same code.

## Setup

Requires Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/ahmadjouni1/AhmadJouni-BusinessAgent-C3.git
cd AhmadJouni-BusinessAgent-C3
pip install -r requirements.txt
cp .env.example .env        # then paste your key into .env as GEMINI_API_KEY=...
```

The app uses the `openai` Python client pointed at Gemini's OpenAI-compatible endpoint
(`https://generativelanguage.googleapis.com/v1beta/openai/`). Models are set at the top of `app.py`:

| Variable | Default | Used for | Override in `.env` |
|---|---|---|---|
| `MODEL` | `gemini-3.8-flash` | the agent (tool calling) | `GEMINI_MODEL` |
| `ROUTER_MODEL` | `gemini-3.5-flash-lite` | intent classification | `GEMINI_ROUTER_MODEL` |
| `REFLECTION_MODEL` | `gemini-3.6-flash` | reflection check | `GEMINI_REFLECTION_MODEL` |

Gemini's free tier rate-limits each model separately (about 5 requests per minute), and one chat turn makes 3 to 4
calls, so the steps are spread across models. If the per-minute limit is hit, `llm()` waits the delay Gemini suggests
and retries (`[RATE LIMIT] ... waiting Ns`). The free tier also caps each model at about **20 requests per day**; when
a model's daily quota runs out, `llm()` switches to the next model in `FALLBACK_MODELS` (`[QUOTA] ... switching model`).
For heavy use, enable billing on your Google AI Studio project.

## Run locally

**Notebook:** open `business_agent.ipynb` and run all cells. You can also run it headless:

```bash
jupyter nbconvert --to notebook --execute --inplace business_agent.ipynb
```

The last cell launches the Gradio chat inline.

**App:**

```bash
python app.py               # opens http://127.0.0.1:7860
```

The console prints `[ROUTER]`, `[TOOL]`, `[DRAFT]` and `[REFLECTION]` lines for every message. Logs are appended to
`leads.jsonl`, `feedback.jsonl` and `reflection.jsonl` in the repo root (set `LOG_DIR` to change this).

**Regenerate assets** (optional):

```bash
python scripts/make_business_pdf.py    # rebuild the PDF
python scripts/build_notebook.py       # rebuild the notebook after editing app.py
```

## Deploy to Hugging Face Spaces

1. Create a new Space at <https://huggingface.co/new-space>, pick **Gradio** as the SDK, and leave it empty.
2. In the Space, open **Settings → Variables and secrets → New secret**, and add `GEMINI_API_KEY` with your key.
3. Push this repo to the Space (the YAML header at the top of this README already configures it):
   ```bash
   git remote add space https://huggingface.co/spaces/<your-hf-user>/<space-name>
   git push space main
   ```
   When asked for a password, use a Hugging Face access token with write permission.
4. The Space installs `requirements.txt` and runs `app.py`. The `me/` folder ships with the repo, so the agent has its documents.

On Spaces the `.jsonl` logs live on the container's temporary disk and reset when the Space restarts. Watch the
**Logs** tab to see the router, tool and reflection lines live.

## Demo

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for a message-by-message script that exercises every route, both tools, a
reflection revision and an Arabizi conversation.

---
*SunCedar Solar, its team, prices, phone numbers and policies are fictional, created for this assignment.*
