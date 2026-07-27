from typing import TypedDict

from langgraph.graph import StateGraph , START , END

# State
class State(TypedDict):
    text : str

# Child Graph
def uppercase_node(state: State):
    return {
        "text" : state["text"].upper()
    }

# Child Graph
child_builder = StateGraph(State)

# Register Node
child_builder.add_node("uppercase",uppercase_node)

# Edges
child_builder.add_edge(START , "uppercase")
child_builder.add_edge("uppercase" , END)

# child Graph with Compile
child_graph = child_builder.compile()

# Parent Graph
parent_builder = StateGraph(State)

# Subgraph ko node ki tarah add karna
parent_builder.add_node("text_processor", child_graph)

# Subgraph Edges
parent_builder.add_edge(START , "text_processor")
parent_builder.add_edge("text_processor" , END)

graph = parent_builder.compile()

# Run
result = graph.invoke(
    {
        "text" : "hello langgraph"
    }
)
print(result)

