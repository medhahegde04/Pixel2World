import os

from groq import Groq
import base64

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Load and encode image
with open(r"C:\Users\surav\Downloads\pixellab-Create-a-pixel-map-of-a-simple-1780406723656.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
            {"type": "text", "text": "What is in this image?"}
        ]
    }]
)

print(response.choices[0].message.content)