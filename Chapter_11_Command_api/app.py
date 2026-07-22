from typing import TypedDict, Literal

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.types import Command

# =====================================================
# State
# =====================================================

class State(TypedDict):
    number: int
    result: str


# =====================================================
# Router Node
# Purpose:
# 1. Decide next node
# 2. Update state
# =====================================================

def router(
    state: State,
) -> Command[Literal["even_node", "odd_node"]]:

    print("State Received :")
    print(state)

    if state["number"] % 2 == 0:

        print("\nDecision : Even Number")
        print("Goto -> even_node")

        return Command(
            update={
                "result": "Even Number"
            },
            goto="even_node"
        )

    print("\nDecision : Odd Number")
    print("Goto -> odd_node")

    return Command(
        update={
            "result": "Odd Number"
        },
        goto="odd_node"
    )


# =====================================================
# Even Node
# =====================================================

def even_node(state: State):

    print("\n========== Even Node ==========")

    print("State Received :")
    print(state)

    print("\nEven Node Executed")

    return {}


# =====================================================
# Odd Node
# =====================================================

def odd_node(state: State):

    print("\n========== Odd Node ==========")

    print("State Received :")
    print(state)

    print("\nOdd Node Executed")

    return {}


# =====================================================
# Create Graph
# =====================================================

builder = StateGraph(State)

builder.add_node(
    "router",
    router,
    destinations=("even_node", "odd_node")
)

builder.add_node("even_node", even_node)

builder.add_node("odd_node", odd_node)

# =====================================================
# Edges
# =====================================================

builder.add_edge(
    START,
    "router"
)

# No edge from router.
# Command(goto=...) decides next node dynamically.

builder.add_edge(
    "even_node",
    END
)

builder.add_edge(
    "odd_node",
    END
)

# =====================================================
# Compile
# =====================================================

graph = builder.compile()

# =====================================================
# Run
# =====================================================

result = graph.invoke(
    {
        "number": 10,
        "result": ""
    }
)

print("\n========== Final State ==========")
print(result)