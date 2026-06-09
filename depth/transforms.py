import numpy as np

def enhance_mountains(depth):
    return np.power(depth, 1.5)

def flatten_terrain(depth):
    return np.power(depth, 0.7)

def deepen_valleys(depth):
    return 1 - np.power(1 - depth, 1.5)

def apply_feedback(depth, feedback):

    if feedback == "mountains too flat":
        return enhance_mountains(depth)

    elif feedback == "terrain too rough":
        return flatten_terrain(depth)

    elif feedback == "valleys too shallow":
        return deepen_valleys(depth)

    return depth