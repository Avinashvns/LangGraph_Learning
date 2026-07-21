from typing import Annotated, TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.graph.message import add_messages

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

# ======================================
# State
# ======================================

class State(TypedDict):

    messages: Annotated[list, add_messages]

# ======================================
# Node 1
# ======================================

def greeting(state: State):

    return {
        "messages": [
            AIMessage(
                content="Hello!"
            )
        ]
    }

# ======================================
# Node 2
# ======================================

def introduction(state: State):

    return {
        "messages": [
            AIMessage(
                content="Welcome to LangGraph."
            )
        ]
    }

# ======================================
# Graph
# ======================================

builder = StateGraph(State)

builder.add_node("greeting", greeting)
builder.add_node("introduction", introduction)

builder.add_edge(START, "greeting")
builder.add_edge("greeting", "introduction")
builder.add_edge("introduction", END)

graph = builder.compile()

# ======================================
# Run
# ======================================

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Hi"
            )
        ]
    }
)

# ======================================
# Print Messages
# ======================================

for message in result["messages"]:
    print(f"{message.type} : {message.content}")