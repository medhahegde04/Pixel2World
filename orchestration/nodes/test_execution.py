import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution import execution_node

fake_depth = [
    [0.9, 0.8, 0.7, 0.6],
    [0.5, 0.4, 0.3, 0.2],
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
]

fake_scene = {
    "regions": [
        {"label": "mountain", "elevation": "high",   "position": "centre",     "dominant_colour": "#FFFFFF"},
        {"label": "forest",   "elevation": "medium", "position": "north",      "dominant_colour": "#228B22"},
        {"label": "water",    "elevation": "low",    "position": "south-east", "dominant_colour": "#1E90FF"},
    ]
}

# case 1: best_depth_map is available 
print("=== Test 1: best_depth_map available ===\n")

fake_state_with_best = {
    "image_path": "test_image.png",
    "scene_description": fake_scene,
    "depth_map": fake_depth,
    "review_pass": True,
    "artifacts": [],
    "iteration": 3,
    "max_iterations": 3,
    "best_depth_map": fake_depth,
    "best_score": 0.82,
    "terrain_sent": False,
}

result1 = execution_node(fake_state_with_best)
print(f"\nexecution_node returned: {result1}")

# case 2: no best_depth_map – fallback to depth_map
print("\n=== Test 2: no best_depth_map — fallback ===\n")

fake_state_no_best = {**fake_state_with_best,
    "best_depth_map": None,
    "best_score": 0.0,
}

result2 = execution_node(fake_state_no_best)
print(f"\nexecution_node returned: {result2}")