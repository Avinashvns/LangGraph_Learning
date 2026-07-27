from typing import TypedDict

from langgraph.graph import StateGraph , START , END

from langgraph.types import interrupt , Command

from langgraph.checkpoint.memory import InMemorySaver

# Create State
class State(TypedDict):
    name : str

# Create Node
def ask_name(state: State):
    print("Node Started")

    name = interrupt("What is your name?")

    print("Resumed....")

    return {
        "name" : name
    }

# Create Graph
builder = StateGraph(State)

# Register Node
builder.add_node("ask_name" , ask_name)

# Add Edges
builder.add_edge(START , "ask_name")
builder.add_edge("ask_name" , END)

# Compile with Memory
graph = builder.compile(
    checkpointer=InMemorySaver()
)

# Config
config = {
    "configurable" : {
        "thread_id" : "thread-1"
    }
}

# First Invoke
result = graph.invoke(
    {},
    config=config
)
print(result)

# Resume Graph
resume = graph.invoke(
    Command(resume="Akash"),
    config=config
)
print(resume)