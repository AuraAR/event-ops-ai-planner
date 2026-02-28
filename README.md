# Event Operations AI Planner

An AI-powered event operations platform that generates comprehensive, structured ops plans for complex events — music festivals, conferences, corporate events, and more. Describe your event in plain language and get a full plan covering staffing, equipment, risk management, timelines, and budget in seconds.

**[→ Live Demo](https://auraAR.github.io/event-ops-ai-planner)**

---

## What It Does

Planning a large-scale event involves coordinating dozens of moving parts across vendors, staff, equipment, and logistics. This tool takes a natural language event description and produces a fully structured operations plan across 7 dimensions:

- **Task Checklist** — prioritized action items with owners and deadlines
- **Staffing Requirements** — roles, headcount, and responsibilities
- **Equipment List** — categorized gear with vendor notes
- **Risk Management** — likelihood/impact matrix with mitigation strategies
- **Timeline Overview** — phased milestones from planning through execution
- **Budget Considerations** — category breakdown with rough allocations
- **Event Summary** — key metadata extracted and structured from your description

Each section is independently refinable — give feedback on any section and the AI regenerates just that part.

---

## Stack

| Layer | Tech |
|-------|------|
| AI Backend | [xAI Grok API](https://x.ai/api) (`grok-3`) via OpenAI-compatible SDK |
| Python CLI | `openai` SDK, structured JSON output, iterative refinement |
| Web Frontend | Vanilla HTML/CSS/JS, no build step required |

The Python backend uses `response_format: json_object` to guarantee structured output rather than parsing free-text, and exposes a `refine_section()` function for targeted iteration without regenerating the full plan.

---

## Getting Started

### CLI

```bash
pip install openai

# Set your xAI API key
export XAI_API_KEY=your_key_here

python planner.py
```

Enter your event description when prompted. The full plan is saved as a timestamped JSON file and printed to the terminal. You'll then be prompted to refine any section interactively.

### Web App

Open `index.html` directly in a browser — no server required. The app calls the AI API client-side. Add your API key in the JS config at the top of the file.

---

## Example

**Input:**
```
3-day electronic music festival in Austin TX, August 2025.
15,000 attendees per day, 4 stages, 60 artists, camping on-site,
VIP section, full catering, merchandise vendors.
```

**Output:** A complete ops plan with ~40 tasks, 18 staff roles, equipment across 8 categories, 12 risk items, 6 timeline phases, and a full budget breakdown — generated in ~3 seconds.

---

## Architecture Notes

- **Grok-3 via OpenAI SDK** — xAI's API is OpenAI-compatible, so migration from GPT-4 required only changing `base_url` and `model`. Grok's extended context window handles large, complex events without truncation.
- **Structured JSON output** — `response_format: json_object` enforces valid JSON at the API level, eliminating fragile parsing of markdown-wrapped responses.
- **Section-level refinement** — rather than regenerating the full plan on each edit, `refine_section()` sends only the relevant section back with user feedback, reducing latency and token cost.
- **Schema-driven prompting** — the full JSON schema is included in the prompt, giving the model an explicit contract to fill rather than inferring structure.

---

## Files

```
├── planner.py              # Python CLI with Grok integration
├── index.html              # Web frontend (single-file, no dependencies)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Roadmap

- [ ] Multi-agent architecture — separate agents for staffing, logistics, and risk
- [ ] Vendor contact database integration
- [ ] PDF/Excel export
- [ ] Event templates (festival, conference, wedding, corporate)
- [ ] Collaborative editing with shared plan URLs

---

## License

MIT
