from langgraph.graph import StateGraph , MessagesState , START , END

from langchain_core.messages import AIMessage

# Node 1
def greet(state: MessagesState):
    return{
        "messages" : [
            AIMessage(content = "Hello!")
        ]
    }

# Node 2
def introduction(state: MessagesState):
    return{
        "messages" : [
            AIMessage(content = "Welcome to LangGraph")
        ]
    }

# Create Graph
graph = StateGraph(MessagesState)

# Register Node
graph.add_node("greet" , greet)
graph.add_node("introduction" ,introduction)

# Connect Node
# START
#   ↓
# greet

graph.add_edge(START , "greet")
graph.add_edge("greet" , "introduction")
graph.add_edge("introduction" , END)

# Compile
app = graph.compile()

# Run Graph
results = app.invoke(
    {
        "messages" : []
    }
)

# print(results)

for message in results["messages"]:
    print(message.content)