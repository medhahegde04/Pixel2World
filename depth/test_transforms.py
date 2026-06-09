from depth.depth_estimator import generate_depth
from depth.normalize import normalize_depth
from depth.transforms import apply_feedback

depth = generate_depth(
    r"C:\Users\surav\Desktop\CP\Depth Estimator\PM 1.jpg"
)

depth = normalize_depth(depth)

new_depth = apply_feedback(
    depth,
    "mountains too flat"
)

print("Original Mean:", depth.mean())
print("Modified Mean:", new_depth.mean())