import json
from state import Pixel2WorldState

# temporary stub function
def send_to_fastapi(depth_map: list, biomes: list) -> bool:
    print("[EXECUTION] WARNING: This is a temporary stub. FastAPI call is not integrated yet.")
    print(f"[EXECUTION] Would send depth map of size {len(depth_map)} x {len(depth_map[0])}")
    print(f"[EXECUTION] Would send {len(biomes)} biome regions")
    return True

def execution_node(state: Pixel2WorldState) -> dict:
    print("[EXECUTION] Preparing terrain data for Unity")
    depth_to_send = state["best_depth_map"] or state["depth_map"]

    if depth_to_send is state["best_depth_map"]:
        print(f"[EXECUTION] Using best_depth_map (score: {state['best_score']:.4f})")
    else:
        print("[EXECUTION] WARNING: No best_depth_map found, falling back to last depth_map")

    biomes = state["scene_description"]["regions"]
    print(f"[EXECUTION] Biomes to apply: {[r['label'] for r in biomes]}")

    # --- to be replaced with actual call ---
    success = send_to_fastapi(
        depth_map=depth_to_send,
        biomes=biomes
    )

    if success:
        print("[EXECUTION] Terrain successfully sent to Unity")
    else:
        print("[EXECUTION] WARNING: FastAPI call failed — terrain may not have reached Unity")

    return {"terrain_sent": success}