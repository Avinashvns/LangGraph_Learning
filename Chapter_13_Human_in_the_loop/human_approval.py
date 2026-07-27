from typing import TypedDict, Literal

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.types import (
    interrupt,
    Command,
)

from langgraph.checkpoint.memory import (
    InMemorySaver,
)


# Crete State
class State(TypedDict):
    task: str
    approval: bool


# Approval Node
def approval_node(
        state: State,
    ) -> Command[Literal["execute_node", "cancel_node"]]:
    approval = interrupt(f"Approve this task?\n\n{state['task']}\n\n(True / False)")
    if approval:

        return Command(
            update={
                "approved": True
            },
            goto="execute_node"
        )

    return Command(
        update={
            "approved": False
        },
        goto="cancel_node"
    )


# Execute Node
def executed_node(state : State):
    print("\nTask Executed")
    print(state["task"])
    return {}

# Cancel Node
def cancel_node(state: State):
    print("\nTask Cancelled")
    return {}

# Build Graph
builder = StateGraph(State)

# Register Node
builder.add_node("approval_node" , approval_node,destinations=("execute_node" , "cancel_node"))
builder.add_node("execute_node", executed_node)
builder.add_node("cancel_node",cancel_node)

# Create Edges
builder.add_edge(START, "approval_node")
builder.add_edge("execute_node" , END)
builder.add_edge("cancel_node" ,END)

# Compile with Memory
graph = builder.compile(
    checkpointer=InMemorySaver()
)

# config
config = {
    "configurable" : {
        "thread_id" : "approval_demo"
    }
}

# First Invoke
result = graph.invoke(
    {
        "task" : "Delete all temporary files",
        "approved" : False
    },
    config = config
)

print("\nInterrupted :")
print(result)

# Resume
result = graph.invoke(
    Command(
        resume=True
    ),
    config=config,
)

print("\nFinal State")
print(result)