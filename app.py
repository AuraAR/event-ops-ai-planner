from openai import OpenAI
import os

# Initialize client
client = OpenAI()

def generate_event_plan(event_description):
    prompt = f"""
    You are an event operations planning assistant.

    Create a structured event operations plan for:
    {event_description}

    Include:
    - Task checklist
    - Staffing requirements
    - Equipment list
    - Risk management considerations
    - Timeline overview

    Keep it clear and structured.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text


if __name__ == "__main__":
    print("=== Event Operations Planner ===\n")
    event_input = input("Describe your event: ")

    print("\nGenerating plan...\n")
    plan = generate_event_plan(event_input)

    print(plan)