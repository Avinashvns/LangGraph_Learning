from typing import TypedDict , Annotated
import operator

from langgraph.graph import StateGraph , START, END
from langgraph.types import Send

# State
class OverallState(TypedDict):
    subjects : list[str]
    jokes : Annotated[list[str] , operator.add]


class JokeState(TypedDict):
    subject : str
   

# Planner
def planner(state: OverallState):
    return {}

# Routing Function
def continue_to_jokes(state: OverallState):
    return [
        Send(
            "generate_joke" , { "subject" : subject}
        )
        for subject in state["subjects"]
    ]

# Worker Node
def generate_joke(state: JokeState):
    return {
        "jokes" : [
            f"Joke about {state["subject"]}"
        ]
    }

# Create Graph
builder = StateGraph(OverallState)

# Register Node
builder.add_node("planner", planner)
builder.add_node("generate_joke", generate_joke)

# Create Edges
builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    continue_to_jokes
)

builder.add_edge("generate_joke", END)

# Compile
graph = builder.compile()


# RUN
result = graph.invoke(
    {
        "subjects" : [
            "Python",
            "SQL",
            "Java"
        ],
        "jokes" : []
    }
)

print(result)