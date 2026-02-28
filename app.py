from openai import OpenAI
import json
import time
from datetime import datetime

client = OpenAI()

def generate_event_plan(event_description):
    prompt = f"""
    You are an event operations planning assistant.

    Create a structured event operations plan for:
    {event_description}

    Return the response in JSON format with the following keys:
    - task_checklist
    - staffing_requirements
    - equipment_list
    - risk_management
    - timeline_overview
    """

    start_time = time.time()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    end_time = time.time()

    output_text = response.output[0].content[0].text
    latency = round(end_time - start_time, 2)

    return output_text, latency


if __name__ == "__main__":
    print("=== Event Operations Planner ===\n")
    event_input = input("Describe your event: ")

    print("\nGenerating plan...\n")

    plan, latency = generate_event_plan(event_input)

    filename = f"event_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write(plan)

    print(plan)
    print(f"\nSaved to {filename}")
    print(f"Response time: {latency} seconds")
