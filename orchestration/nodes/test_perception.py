import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perception import perception_node

fake_state = {
    "image_path": "test_image.png",
    "scene_description": None,
    "depth_map": None,
    "review_pass": False,
    "artifacts": [],
    "iteration": 0,
    "max_iterations": 3,
    "best_depth_map": None,
    "best_score": 0.0,
    "terrain_sent": False,
}

print("=== Testing Perception Node ===\n")
result = perception_node(fake_state)

print("\n=== Result ===")
print(f"Keys returned: {list(result.keys())}")
print(f"Number of regions: {len(result['scene_description']['regions'])}")
print("\nFull scene description:")
for region in result["scene_description"]["regions"]:
    print(f"  - {region['label']} ({region['elevation']} elevation) at {region['position']} — {region['dominant_color']}")