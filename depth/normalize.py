import numpy as np

def normalize_depth(depth):

    depth = depth.astype(np.float32)

    normalized = (
        depth - depth.min()
    ) / (
        depth.max() - depth.min()
    )

    return normalized