from typing import Annotated

from langchain_core.tools import tool

from langchain_ollama import ChatOllama

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


# ==========================================
# State
# ==========================================

class State(dict):
    messages: Annotated[list, add_messages]


# ==========================================
# Tool
# ==========================================

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.
    """
    return a * b


tools = [multiply]

# ==========================================
# LLM
# ==========================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
).bind_tools(tools)

# ==========================================
# Chatbot Node
# ==========================================

def chatbot(state):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ==========================================
# Tool Node
# ==========================================

tool_node = ToolNode(tools)

# ==========================================
# Graph
# ==========================================

builder = StateGraph(State)

builder.add_node(
    "chatbot",
    chatbot,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_edge(
    START,
    "chatbot",
)

builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

builder.add_edge(
    "tools",
    "chatbot",
)

graph = builder.compile()

# ==========================================
# Run
# ==========================================

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="What is 25 multiplied by 12?"
            )
        ]
    }
)

for message in result["messages"]:
    print(message)