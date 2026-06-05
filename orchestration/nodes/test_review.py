import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from review import review_node, parse_review_response

# test parse_review_response directly
print("=== Testing parse_review_response ===\n")

# case 1: clean JSON 
raw1 = '{"pass": false, "artifacts": ["inverted elevation in centre"]}'
result1 = parse_review_response(raw1)
print(f"Case 1 (clean JSON):       pass={result1['pass']}, artifacts={result1['artifacts']}")

# case 2: markdown code block (model wrapped the JSON)
raw2 = '```json\n{"pass": true, "artifacts": []}\n```'
result2 = parse_review_response(raw2)
print(f"Case 2 (markdown fences):  pass={result2['pass']}, artifacts={result2['artifacts']}")

# case 3: string booleans (model returned "true" instead of true)
raw3 = '{"pass": "false", "artifacts": ["blurred boundaries"]}'
result3 = parse_review_response(raw3)
print(f"Case 3 (string boolean):   pass={result3['pass']}, artifacts={result3['artifacts']}")

# case 4: broken JSON (model returned garbage)
raw4 = 'Sorry, I could not analyse the image.'
result4 = parse_review_response(raw4)
print(f"Case 4 (broken JSON):      pass={result4['pass']}, artifacts={result4['artifacts']}")

# case 5: missing artifacts key
raw5 = '{"pass": false}'
result5 = parse_review_response(raw5)
print(f"Case 5 (missing artifacts): pass={result5['pass']}, artifacts={result5['artifacts']}")

# test review_node with fake state 
print("\n=== Testing review_node (iteration 1 — stub, should fail) ===\n")

fake_state_iter1 = {
    "image_path": "test_image.png",
    "scene_description": None,
    "depth_map": [[0.5, 0.4], [0.3, 0.2]],   # minimal fake depth map
    "review_pass": False,
    "artifacts": [],
    "iteration": 1,
    "max_iterations": 3,
    "best_depth_map": None,
    "best_score": 0.0,
    "terrain_sent": False,
}

result_node = review_node(fake_state_iter1)
print(f"\nreview_node returned: {result_node}")

# test with no-depth-map 
print("\n=== Testing review_node (no depth map — should fail safe) ===\n")

fake_state_no_depth = {**fake_state_iter1, "depth_map": None}
result_guard = review_node(fake_state_no_depth)
print(f"review_node returned: {result_guard}")