from typing import TypedDict , Annotated
import operator

from langgraph.graph import StateGraph , START , END

# State
class State(TypedDict):
    numbers : Annotated[list[int], operator.add]

# Node 1
def node1(state: State):
    return {
        "numbers" : [1,2]
    }

# Node 2
def node2(state: State):
    return {
        "numbers" : [3,4]
    }

# Create Graph
builder = StateGraph(State)

# Register Nodes
builder.add_node("node1", node1)
builder.add_node("node2", node2)

# Create Edges
builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)

# Compile
graph = builder.compile()

# RUN
result = graph.invoke(
    {
        "numbers" : []
    }
)

print(result)