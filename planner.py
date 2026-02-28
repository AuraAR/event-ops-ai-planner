from openai import OpenAI
import json
import time
from datetime import datetime
from typing import Optional

# xAI Grok API — drop-in OpenAI-compatible client
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1",
)

SYSTEM_PROMPT = """You are an expert event operations planner with deep experience in large-scale events
including music festivals, corporate conferences, and sporting events.

You coordinate complex logistics across vendors, staff, equipment, and timelines.
Always respond with valid JSON only — no markdown fences, no extra text."""

PLAN_SCHEMA = """
{
  "event_summary": {
    "name": "string",
    "type": "string",
    "estimated_attendance": "string",
    "key_dates": ["string"]
  },
  "task_checklist": [
    {
      "category": "string",
      "task": "string",
      "owner": "string",
      "due": "string",
      "priority": "high|medium|low"
    }
  ],
  "staffing_requirements": [
    {
      "role": "string",
      "headcount": "number",
      "responsibilities": ["string"],
      "notes": "string"
    }
  ],
  "equipment_list": [
    {
      "category": "string",
      "items": ["string"],
      "vendor_notes": "string"
    }
  ],
  "risk_management": [
    {
      "risk": "string",
      "likelihood": "high|medium|low",
      "impact": "high|medium|low",
      "mitigation": "string"
    }
  ],
  "timeline_overview": [
    {
      "phase": "string",
      "timeframe": "string",
      "milestones": ["string"]
    }
  ],
  "budget_considerations": [
    {
      "category": "string",
      "notes": "string",
      "rough_percentage": "string"
    }
  ]
}
"""


def generate_event_plan(event_description: str, stream: bool = False) -> tuple[dict, float]:
    """
    Generate a structured event operations plan using Grok.

    Args:
        event_description: Natural language description of the event.
        stream: Whether to stream the response (useful for large events).

    Returns:
        Tuple of (parsed plan dict, latency in seconds)
    """
    prompt = f"""Create a comprehensive event operations plan for the following event:

{event_description}

Return your response as a JSON object matching this exact schema:
{PLAN_SCHEMA}

Be specific, practical, and tailor every detail to the event described."""

    start_time = time.time()

    response = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    latency = round(time.time() - start_time, 2)
    raw = response.choices[0].message.content

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Grok returned invalid JSON: {e}\n\nRaw output:\n{raw}")

    return plan, latency


def refine_section(plan: dict, section: str, feedback: str) -> dict:
    """
    Iteratively refine a specific section of an existing plan based on user feedback.

    Args:
        plan: The existing full plan dict.
        section: Which section to refine (e.g. "staffing_requirements").
        feedback: User's feedback or additional requirements.

    Returns:
        Updated plan dict with the refined section.
    """
    if section not in plan:
        raise ValueError(f"Section '{section}' not found in plan. Available: {list(plan.keys())}")

    prompt = f"""Here is the current '{section}' section of an event operations plan:

{json.dumps(plan[section], indent=2)}

The user wants to refine it with this feedback:
{feedback}

Return ONLY the updated '{section}' as valid JSON (same structure, improved content).
No extra keys, no explanation."""

    response = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    updated_section = json.loads(raw)

    # Handle case where model wraps in outer key
    if section in updated_section:
        updated_section = updated_section[section]

    plan[section] = updated_section
    return plan


def save_plan(plan: dict, filename: Optional[str] = None) -> str:
    """Save plan to a timestamped JSON file."""
    if not filename:
        filename = f"event_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(plan, f, indent=2)
    return filename


def pretty_print_plan(plan: dict) -> None:
    """Print a human-readable summary of the plan."""
    summary = plan.get("event_summary", {})
    print(f"\n{'='*60}")
    print(f"  {summary.get('name', 'Event Plan').upper()}")
    print(f"  {summary.get('type', '')} | {summary.get('estimated_attendance', '')}")
    print(f"{'='*60}\n")

    sections = [
        ("task_checklist", "TASK CHECKLIST"),
        ("staffing_requirements", "STAFFING"),
        ("equipment_list", "EQUIPMENT"),
        ("risk_management", "RISK MANAGEMENT"),
        ("timeline_overview", "TIMELINE"),
        ("budget_considerations", "BUDGET"),
    ]

    for key, label in sections:
        if key not in plan:
            continue
        print(f"--- {label} ---")
        items = plan[key]
        for item in items[:3]:  # Preview first 3
            if isinstance(item, dict):
                first_val = next(iter(item.values()), "")
                print(f"  • {first_val}")
        if len(items) > 3:
            print(f"  ... and {len(items) - 3} more")
        print()


if __name__ == "__main__":
    print("=== Event Operations AI Planner (powered by Grok) ===\n")
    event_input = input("Describe your event: ")
    print("\nGenerating plan with Grok...\n")

    plan, latency = generate_event_plan(event_input)
    pretty_print_plan(plan)

    filename = save_plan(plan)
    print(f"Full plan saved to: {filename}")
    print(f"Response time: {latency}s")

    while True:
        print("\nWould you like to refine a section?")
        print("Sections:", list(plan.keys()))
        section = input("Enter section name (or 'done' to exit): ").strip()
        if section.lower() == "done":
            break
        feedback = input("What would you like to change? ")
        plan = refine_section(plan, section, feedback)
        print(f"\n✓ '{section}' updated.")
        save_plan(plan, filename)
        print(f"Saved to {filename}")
