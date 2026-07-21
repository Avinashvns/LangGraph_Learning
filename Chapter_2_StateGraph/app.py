from typing import TypedDict

from langgraph.graph import StateGraph

# Create State
class GraphState(TypedDict):
    message: str


# Node
def chatbot(state: GraphState):

    print("Node Executed")

    return {
        "message" : "Hello from LangGraph"
    }

# Create Graph
graph = StateGraph(GraphState)

# Add Node
graph.add_node( "chatbot" , chatbot)

# Connect Nodes
    #  Entry Point

graph.set_entry_point("chatbot")

    # Finish Point
graph.set_finish_point("chatbot")

# Compile
app = graph.compile()

# RUN
result = app.invoke(
    {
        "message" : ""
     }
)
print(result)