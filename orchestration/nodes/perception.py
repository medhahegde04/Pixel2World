import os
import base64
import json
from groq import Groq
from dotenv import load_dotenv
from state import Pixel2WorldState

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_VISION_API_KEY"))

def encode_image(image_path: str) -> str:
    """
    Encodes an image to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def parse_json_response(raw: str) -> dict:
    """
    Parses the response from the Groq API as JSON.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1])
    return json.loads(cleaned)

def perception_node(state: Pixel2WorldState) -> dict:
    print(f"[PERCEPTION] Analyzing image: {state['image_path']}")
    image_b64 = encode_image(state["image_path"])
    prompt = """You are a terrain analysis assistant for a game development pipeine.
    Analyze this 2D pixel map and identify the terrain regions.
    Respond ONLY with a valid JSON object. No explanation, no markdown, no preamble.
    Use exactly this structure:
    
    {
        "regions": [
            {
                "label": "<terrain type e.g. mountain, forest, water, grassland, desert>",
                "elevation": "<elevation level e.g. low, medium, high>",
                "position": "<where in the image e.g. center, north, southeast, southwest, etc.>",
                "dominant_color": "<the main hex color in the region e.g. #aabbcc>"
            }
        ]
    }
    
    Identify every distinct terrain region you can see. Be specific about positions."""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    },

                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        temperature = 0.1,
        max_tokens = 500
    )

    raw = response.choices[0].message.content

    try:
        scene = parse_json_response(raw)
    except json.JSONDecodeError as e:
        print(f"[PERCEPTION] WARNING: Failed to parse JSON response: {e}")
        print(f"[PERCEPTION] Raw response: \n{raw}")
        scene = {"regions": []}

    print(f"[PERCEPTION] Detected regions: {len(scene.get('regions', []))}")
    return {"scene_description": scene}