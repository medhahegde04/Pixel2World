from typing import Optional, TypedDict, List

class Pixel2WorldState(TypedDict):
    #input
    image_path: str

    #output (perception)
    scene_description: Optional[dict]

    #output (inference)
    depth_map: Optional[list]

    #review
    review_pass: bool
    artifacts: List[str]

    #loop control
    iteration: int
    max_iterations: int

    #tracking best results
    best_depth_map: Optional[list]
    best_score: float

    #output (execution)
    terrain_sent: bool