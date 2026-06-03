from graph import graph

initial_state = {
    "image_path": "test.png",
    "scene_description": None,
    "depth_map": None,
    "review_pass": False,
    "artifacts": [],
    "iteration": 0,
    "max_iterations": 4,
    "best_depth_map": None,
    "best_score": 0.0,
    "terrain_sent": False,
}

print("=== Starting Pixel2World Pipeline ===\n")
final_state = graph.invoke(initial_state)

print("\n=== Pipeline Complete ===")
print(f"Total iterations:  {final_state['iteration']}")
print(f"Review passed:     {final_state['review_pass']}")
print(f"Best score:        {final_state['best_score']:.2f}")
print(f"Terrain sent:      {final_state['terrain_sent']}")
print(f"Final artifacts:   {final_state['artifacts']}")