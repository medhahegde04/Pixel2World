from depth.depth_estimator import generate_depth
from depth.normalize import normalize_depth
from PIL import Image
import numpy as np

depth = generate_depth(
    r"C:\Users\surav\Desktop\CP\Depth Estimator\PM 1.jpg"
)

print("Original")
print("Shape:", depth.shape)
print("Min:", depth.min())
print("Max:", depth.max())

normalized = normalize_depth(depth)

print("\nNormalized")
print("Min:", normalized.min())
print("Max:", normalized.max())

img = Image.fromarray(
    (normalized * 255).astype(np.uint8)
)

img.save("normalized_depth.png")