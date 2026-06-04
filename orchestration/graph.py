from langgraph.graph import StateGraph, START, END
from state import Pixel2WorldState
from nodes.perception import perception_node 

# --- Stub Nodes ---
# placeholders to test logic

def inference_node(state: Pixel2WorldState) -> dict:
    current_iteration = state["iteration"] + 1
    print(f"[INFERENCE] Running depth estimation - iteration {current_iteration}")
    print(f"[INFERENCE] Artifacts from last review: {state['artifacts']}")

    # future update: run DepthAnything V2
    # currently testing with fake depth map

    fake_depth_map = [
        [0.9, 0.8, 0.7, 0.6],
        [0.5, 0.4, 0.3, 0.2],
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8],
    ]
    score_by_iteration = {
        1: 0.6,
        2: 0.8,
        3: 0.5
    }
    fake_score = score_by_iteration.get(current_iteration, 0.5)
    updates = {
        "depth_map": fake_depth_map,
        "iteration": current_iteration,
    } 
    if fake_score > state["best_score"]:
        updates["best_depth_map"] = fake_depth_map
        updates["best_score"] = fake_score

    return updates


def review_node(state: Pixel2WorldState) -> dict:
    print(f"[REVIEW] Checking depth map quality - iteration {state['iteration']}")
    
    # future update: call Llama 3.2-Vision as a quality critic
    # currently testing with fake review logic (fail first 2 iterations, pass on 3rd)

    if state["iteration"] < 3:
        print("[REVIEW] FAILED - fake artifact detected")
        return {
            "review_pass": False,
            "artifacts": ["inverted elevation in center region"]
        }
    else:
        print("[REVIEW] PASSED")
        return {
            "review_pass": True,
            "artifacts": []
        }
    

def execution_node(state: Pixel2WorldState) -> dict:
    print(f"[EXECUTION] Sending terrain data to Unity via FastAPI")
    depth_to_send = state["best_depth_map"] or state["depth_map"]
    print(f"[EXECUTION] Using best_depth_map: {depth_to_send is state['best_depth_map']} with score {state['best_score']}")
    print(f"[EXECUTION] Biomes to apply: {[r['label'] for r in state['scene_description']['regions']]}")
    
    # future update: send data to FastAPI endpoint
    # currently testing with fake execution logic

    return {
        "terrain_sent": True
    }



# --- Routing Function ---

def route_after_review(state: Pixel2WorldState) -> str:
    if state["review_pass"]:
        print("[ROUTER] Review passed, routing to execution")
        return "execution"
    
    if state["iteration"] >= state["max_iterations"]:
        print(f"[ROUTER] Max iterations ({state['max_iterations']}) reached, routing to execution with best results")
        return "execution"
    
    print(f"[ROUTER] Review failed, routing back to inference for iteration {state['iteration'] + 1}")
    return "inference"



# --- Graph Definition ---

builder = StateGraph(Pixel2WorldState)

# register nodes
builder.add_node("perception", perception_node)
builder.add_node("inference", inference_node)
builder.add_node("review", review_node)
builder.add_node("execution", execution_node)

# register edges
builder.add_edge(START, "perception")
builder.add_edge("perception", "inference")
builder.add_edge("inference", "review")
builder.add_edge("execution", END)

# agentic loop 
# conditional edge from review 
builder.add_conditional_edges(
    "review", 
    route_after_review,
    {
        "inference": "inference",
        "execution": "execution",
    }
)

graph = builder.compile()


"""
Visulaizing the graph using mermaid live editor.
>>> if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())

Output that can be copy-pasted into mermaid live editor to visualize the graph:
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        perception(perception)
        inference(inference)
        review(review)
        execution(execution)
        __end__([<p>__end__</p>]):::last
        __start__ --> perception;
        inference --> review;
        perception --> inference;
        review -.-> execution;
        review -.-> inference;
        execution --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
