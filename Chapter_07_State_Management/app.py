from typing import TypedDict

from langgraph.graph import StateGraph , START , END

# State
class  UserState(TypedDict):
    name : str
    age : int
    city : str

# Node 1
def set_name(state: UserState):
    print("\nNode 1 Received State :")
    print(state)

    return { "name" : "Avinash" }

# Node 2 
def set_age(state: UserState):
    print("\nNode 2 Received State :")
    print(state)

    return { "age" : 32 }

# Node 3
def set_city(state: UserState):
    print("\nNode 3 Received State :")
    print(state)
    return { "city" : "Varanasi" }

# Create Graph
builder = StateGraph(UserState)

builder.add_node("set_name" , set_name)
builder.add_node("set_age", set_age)
builder.add_node("set_city" , set_city)

# Create Edges
builder.add_edge(START , "set_name")
builder.add_edge("set_name", "set_age")
builder.add_edge("set_age", "set_city")
builder.add_edge("set_city" , END)

# Compile
graph = builder.compile()

# RUN
result = graph.invoke(
    {
        "name" : "",
        "age" : 0,
        "city" : ""
    }
)

# Print
print("\nFinal State")
print(result)