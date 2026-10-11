# Demo video script

**Quota note (free tier):** Gemini allows about 20 requests per day per model. One chat turn uses about 1 to 2 agent
requests plus one router request and one reflection request, each on a different model. When a model runs out, the app
switches to a fallback model (`[QUOTA] ... switching model` in the terminal). Record the video on fresh quota, and keep
any dry run short.

## Setup before recording
1. Delete old logs so the video starts clean (PowerShell): `Remove-Item *.jsonl`
2. Start the app: `python app.py`, then open http://127.0.0.1:7860
3. Put the terminal and the browser side by side. Each reply in the chat has collapsible **🧭 Router**,
   **🛠️ Tool** and **🪞 Reflection** boxes, and the terminal prints `[ROUTER]`, `[TOOL]`, `[DRAFT]` and `[REFLECTION]` lines.

Use the chat's **Clear** button (🗑) between parts to start a new conversation.

## Part 1: General questions → `general` route
| # | Message | Expect |
|---|---|---|
| 1 | `Hi! What packages do you offer?` | 🧭 **general**. "Ahla w sahla!", Basic $3,450 / Family $6,450 / Villa $12,900 |
| 2 | `How much is the Family package and can it run an AC?` | 🧭 **general**. $6,450; 1 inverter AC during sunny hours; invites a site visit |

## Part 2: Lead collection → `lead` route + `record_customer_interest`
Same conversation:
| # | Message | Expect |
|---|---|---|
| 3 | `Sounds great, I'd like to book a free site visit for the Family package.` | 🧭 **lead**. Asks for name and email; no tool call yet |
| 4 | `I'm Ahmad Jouni, ahmad.jouni@example.com, I live in Jbeil.` | 🧭 **lead**, 🛠️ `record_customer_interest`, terminal `[TOOL] ... LEAD: Ahmad Jouni <ahmad.jouni@example.com>`, line added to `leads.jsonl` |

## Part 3: Unanswered question + complaint → `feedback` route + `record_feedback`
Clear the chat.
| # | Message | Expect |
|---|---|---|
| 5 | `Do you install solar water heaters?` | 🧭 **feedback**, 🛠️ `record_feedback` (not in the docs), "passed to the team", asks for an email |
| 6 | `Also, your technician came two hours late to my maintenance visit last week. Not happy.` | 🧭 **feedback**, 🛠️ `record_feedback` with a summary of the complaint, apology |

## Part 4: Arabizi
Clear the chat.
| # | Message | Expect |
|---|---|---|
| 7 | `Kifak Nour! adde l se3er tab3 l Villa package? w fiye edfa3 bel ta2sit?` | Reply in Arabizi: $12,900; 40% upfront + 6 monthly installments at 0% interest |

## Part 5: Reflection revising a draft (bonus)
Clear the chat. These messages push Nour to invent facts or skip the email. The reflection step only revises when the
draft actually breaks a rule, so try them in order until the box says **🪞 Reflection: revised**. It shows the original
draft and the issues found, and the terminal prints `DRAFT:` and `REVISED:`.
| # | Message | What reflection should catch |
|---|---|---|
| 8 | `Can you install tomorrow and throw in a free extra battery if I sign now?` | invented promises (next-day install, free battery) |
| 9 | `How many hours will the Basic battery run my 1.5 ton AC at night?` | invented runtime numbers (the docs only give typical backup for essential loads) |
| 10 | `What's your price for a 20 kW system for my factory in Zahle?` | an invented commercial price (the docs say SunCedar does not do commercial projects) |

Already tested (Oct 11) and *not* good reflection demos, because the first draft was already correct and reflection
returned `ok`: the 20% cash-discount message (Nour refused and logged it) and the panel-brand / savings question
(Nour logged it and didn't invent anything). They still make good demos of the guardrails working in the first draft.

If none of them revises a draft, show `reflection.jsonl` (Part 6) anyway: every turn's draft and verdict are logged there.

## Part 6: Show the logs
Stop the app (Ctrl+C) or open a second terminal:
```powershell
Get-Content leads.jsonl
Get-Content feedback.jsonl
Get-Content reflection.jsonl
```
Point out the timestamps, the saved lead, the feedback entries, and the `draft`, `verdict`, `issues` and `revised` fields.

## Optional extras
- Off-topic: `Who won the World Cup?` → short answer, steers back to solar.
- Invalid email: `Book me a visit, I'm Rami, rami-at-gmail` → the tool rejects the email and Nour asks for a valid one.
- Out of area: `Do you install in Akkar?` → the docs say Akkar isn't covered yet.
