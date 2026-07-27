from typing import TypedDict, Literal

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.types import Command

from langchain_ollama import ChatOllama

# LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# State
class State(TypedDict):
    question: str
    answer: str


# Supervisor
def supervisor(
    state: State,
) -> Command[
    Literal[
        "research_agent",
        "summary_agent",
        "translation_agent",
    ]
]:
    prompt = f"""
You are a supervisor.

Choose ONLY ONE worker.

Workers:

research_agent
summary_agent
translation_agent

Question:

{state["question"]}

Return only worker name.
"""

    decision = llm.invoke(prompt).content.strip().lower()

    if decision == "research_agent":
        return Command(goto="research_agent")

    elif decision == "summary_agent":
        return Command(goto="summary_agent")

    else:
        return Command(goto="translation_agent")


# Research Agent
def research_agent(state: State):
    return {"answer": "Research Completed"}


# Summary Agent
def summary_agent(state: State):
    return {"answer": "Summary Completed"}


# Translation Agent
def translation_agent(state: State):
    return {"answer": "Translation Completed"}


# Graph
builder = StateGraph(State)

# Register Node
builder.add_node(
    "supervisor",
    supervisor,
    destinations=(
        "research_agent",
        "summary_agent",
        "translation_agent",
    ),
)

builder.add_node(
    "research_agent",
    research_agent,
)

builder.add_node(
    "summary_agent",
    summary_agent,
)

builder.add_node(
    "translation_agent",
    translation_agent,
)

# Edges
builder.add_edge(
    START,
    "supervisor",
)

builder.add_edge(
    "research_agent",
    END,
)

builder.add_edge(
    "summary_agent",
    END,
)

builder.add_edge(
    "translation_agent",
    END,
)

# Compile
graph = builder.compile()

# Run
result = graph.invoke(
    {
        "question": "Translate Hello into Hindi",
        "answer": "",
    }
)

print(result)
