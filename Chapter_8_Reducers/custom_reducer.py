from typing import TypedDict, Annotated

from langgraph.graph import (
    StateGraph,
    START,
    END
)

# ======================================
# Custom Reducer
# ======================================

def max_score(old: int, new: int) -> int:
    return max(old, new)

# ======================================
# State
# ======================================

class State(TypedDict):

    score: Annotated[int, max_score]

# ======================================
# Node 1
# ======================================

def node1(state: State):

    return {
        "score": 80
    }

# ======================================
# Node 2
# ======================================

def node2(state: State):

    return {
        "score": 95
    }

# ======================================
# Graph
# ======================================

builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)

graph = builder.compile()

# ======================================
# Run
# ======================================

result = graph.invoke(
    {
        "score": 0
    }
)

print(result)