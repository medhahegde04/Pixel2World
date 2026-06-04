import os

from groq import Groq
import base64
import json

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_map(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    # detect format from extension
    ext = image_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/webp" if ext == "webp" else "image/png"
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_data}"}},
                {"type": "text", "text": """Analyze this pixel art game map and extract terrain features.
                Respond ONLY in valid JSON, no extra text:
                {
                    "terrain_types": ["list of terrains present e.g. forest, mountain, water, beach, lava"],
                    "dominant_terrain": "main terrain type",
                    "complexity": "low/medium/high",
                    "features": ["notable landmarks or structures"],
                    "walkable_areas": ["describe walkable zones"],
                    "hazards": ["dangerous or unwalkable areas"]
                }"""}
            ]
        }]
    )
    
    raw = response.choices[0].message.content
    # strip markdown code blocks if present
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

print("=== MAP 1 ===")
result1 = analyze_map(r"C:\Users\surav\Desktop\llama-vision\PM 1.jpg")
print(json.dumps(result1, indent=2))

print("\n=== MAP 2 ===")
result2 = analyze_map(r"C:\Users\surav\Desktop\llama-vision\PM 2.webp")
print(json.dumps(result2, indent=2))