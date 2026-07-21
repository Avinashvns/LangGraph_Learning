from langgraph.graph import ( StateGraph , MessagesState , START , END)
from langchain_core.messages import AIMessage

# Node 1
def greet(state: MessagesState):

    return {
        "messages": [
            AIMessage(
                content="Hello!"
            )
        ]
    }

# Node 2
def introduction(state: MessagesState):

    return {
        "messages": [
            AIMessage(
                content="Welcome to LangGraph."
            )
        ]
    }

# Node 3 
def goodbye(state: MessagesState):

    return {
        "messages": [
            AIMessage(
                content="Good Bye!"
            )
        ]
    }

# Create Graph
graph = StateGraph(MessagesState)

# Register Nodes
graph.add_node("greet" , greet)
graph.add_node("introduction", introduction)
graph.add_node("goodbye", goodbye)

# Edges

graph.add_edge(START, "greet")

graph.add_edge("greet", "introduction")

graph.add_edge("introduction", "goodbye")

graph.add_edge("goodbye", END)

# Compile
app = graph.compile()

# RUN
results = app.invoke(
    {
        "messages" : []
    }
)

# print Message
for message in results["messages"]:
    print(message.content)