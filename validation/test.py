import os

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": "Hello! What can you do?"}]
)

print(response.choices[0].message.content)