import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, TOOL_MAP

load_dotenv()
client = OpenAI()

def run_agent(task, max_iterations=10):
    print(f"\nTask: {task}")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful agent with access to tools. Use them to complete tasks accurately. When the task is fully complete, provide a final answer without calling any more tools."
        },
        {"role": "user", "content": task}
    ]

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"\nFinal Answer: {message.content}")
            return message.content

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"\n[Tool call] {tool_name}({tool_args})")

            if tool_name in TOOL_MAP:
                result = TOOL_MAP[tool_name](**tool_args)
            else:
                result = f"Error: tool {tool_name} not found"

            print(f"[Result] {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "Max iterations reached"

if __name__ == "__main__":
    run_agent("What time is it right now?")
    run_agent("List all Python files in the current directory, then tell me how many lines the first one has.")
    run_agent("Find all Python files in the parent directory, then scan the most suspicious-looking one for security vulnerabilities, and give me a summary of what you found.")
    run_agent("What files have we scanned recently and what were their risk levels?")