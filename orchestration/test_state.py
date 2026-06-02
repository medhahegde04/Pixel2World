from state import Pixel2WorldState

state = Pixel2WorldState(
    image_path="test.png",
    scene_description=None,
    depth_map=None,
    review_pass=False,
    artifacts=[],
    iteration=0,
    max_iterations=5,
    best_depth_map=None,
    best_score=0.0,
    terrain_sent=False,
)

print(state)