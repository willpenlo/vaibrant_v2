import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI()  # Automatically picks up the API key from the environment variable

response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Say hello and tell me what can I help with. Use a tone that is similar to a british butler. Do not use more than 20 words."
        }
    ]
)
print(response.choices[0].message.content)
