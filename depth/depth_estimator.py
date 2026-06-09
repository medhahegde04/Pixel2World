from transformers import pipeline
from PIL import Image
import numpy as np

depth_pipe = pipeline(
    task="depth-estimation",
    model="depth-anything/Depth-Anything-V2-Small-hf"
)

def generate_depth(image_path):
    image = Image.open(image_path)

    result = depth_pipe(image)

    depth = np.array(result["depth"])

    return depth