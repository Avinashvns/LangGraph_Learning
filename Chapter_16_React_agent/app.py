from typing import Annotated

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)

from langchain_core.messages import HumanMessage

from langchain_core.tools import tool

from langchain_ollama import ChatOllama


# ======================================
# State
# ======================================

class State(dict):
    messages: Annotated[list, add_messages]


# ======================================
# Tools
# ======================================

@tool
def multiply(a: int, b: int):
    """Multiply two numbers."""
    return a * b


@tool
def square(number: int):
    """Square a number."""
    return number * number


tools = [multiply, square]

# ======================================
# LLM
# ======================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
).bind_tools(tools)

# ======================================
# Agent Node
# ======================================

def agent(state):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ======================================
# Tool Node
# ======================================

tool_node = ToolNode(tools)

# ======================================
# Graph
# ======================================

builder = StateGraph(State)

builder.add_node("agent", agent)

builder.add_node("tools", tool_node)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge(
    "tools",
    "agent"
)

graph = builder.compile()

# ======================================
# Run
# ======================================

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Multiply 12 by 5 and then square the answer."
            )
        ]
    }
)

for message in result["messages"]:
    print(message)