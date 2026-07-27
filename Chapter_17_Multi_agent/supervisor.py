from typing import TypedDict, Literal

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.types import Command

# Create State

class State(TypedDict):
    question: str
    research: str
    summary: str
    translation: str
    step: str

# Create Supervisor Node
def supervisor(
    state: State,
) -> Command[
    Literal[
        "research_agent",
        "summary_agent",
        "translation_agent",
        END,
    ]
]:

    step = state["step"]

    if step == "research":
        return Command(goto="research_agent")

    elif step == "summary":
        return Command(goto="summary_agent")

    elif step == "translation":
        return Command(goto="translation_agent")

    return Command(goto=END)

# Create Research Agent Node
def research_agent(state: State):

    print("Research Agent")

    return {
        "research": f"Research about {state['question']}",
        "step": "summary",
    }

# Create Summary agent Node
def summary_agent(state: State):

    print("Summary Agent")

    return {
        "summary": "Short Summary",
        "step": "translation",
    }

# Create Translation Agent Node
def translation_agent(state: State):

    print("Translation Agent")

    return {
        "translation": "Hindi Translation",
        "step": "finish",
    }

# Create Graph
builder = StateGraph(State)

# Register Node
builder.add_node(
    "supervisor",
    supervisor,
    destinations=(
        "research_agent",
        "summary_agent",
        "translation_agent",
        END,
    ),
)

builder.add_node("research_agent", research_agent)
builder.add_node("summary_agent", summary_agent)
builder.add_node("translation_agent", translation_agent)

# Edges
builder.add_edge(START, "supervisor")

builder.add_edge("research_agent", "supervisor")
builder.add_edge("summary_agent", "supervisor")
builder.add_edge("translation_agent", "supervisor")

# Compile
graph = builder.compile()

# Run
result = graph.invoke(
    {
        "question": "Artificial Intelligence",
        "research": "",
        "summary": "",
        "translation": "",
        "step": "research",
    }
)

print(result)