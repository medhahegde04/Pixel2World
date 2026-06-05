import json
from state import Pixel2WorldState

# temporary stub node
def call_llama_critic(original_image_path: str, depth_map_list: list) -> str:
    print("[REVIEW] WARNING: This is a temporary stub node. The actual implementation of the llama critic is not yet available.")

    return '{"pass": false, "artifacts": ["stub artifact 1", "stub artifact 2"]}'


def parse_review_response(raw: str) -> dict:
    """
    Parses the raw string returned by the Llama critic call.

    Handles two failure cases:
    1. Model wraps JSON in markdown code block, e.g. ```json ... ```
    2. Model returns something unparseable

    In both cases we return a failed review with an artifact indicating the issue rather than crashing the entire pipeline.
    """
    cleaned = raw.strip()

    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"[REVIEW] WARNING: JSON parse failed: {e}")
        print(f"[REVIEW] Raw response was: \n{raw}")

        return {
            "pass": False,
            "artifacts": ["review response could not be parsed as JSON — retrying"]
        }
    
    if "pass" not in parsed:
        print("[REVIEW] WARNING: 'pass' key not found in review response. Defaulting to fail.")
        parsed["pass"] = False
    
    if "artifacts" not in parsed:
        parsed["artifacts"] = []

    if isinstance(parsed["pass"], str):
        parsed["pass"] = parsed["pass"].lower() == "true"

    return parsed


def review_node(state: Pixel2WorldState) -> dict:
    print(f"[REVIEW] Checking depth map quality. Iteration: {state['iteration']}")

    if state["depth_map"] is None:
        print("[REVIEW] WARNING: No depth map in state. Failing review.")
        return {
            "review_pass": False,
            "artifacts": ["no depth map available to review"]
        }
    
    # --- to be replaced with actual call ---
    raw_response = call_llama_critic(
        original_image_path = state["image_path"],
        depth_map_list = state["depth_map"]
    )

    result = parse_review_response(raw_response)

    if result["pass"]:
        print("[REVIEW] PASSED")
    else:
        print(f"[REVIEW] FAILED — artifacts: {result['artifacts']}")
    
    return {
        "review_pass": result["pass"],
        "artifacts":   result["artifacts"]
    }