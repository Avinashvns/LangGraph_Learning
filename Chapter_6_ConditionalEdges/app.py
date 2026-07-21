from langgraph.graph import StateGraph, MessagesState , START , END
from langchain_core.messages import AIMessage , HumanMessage

# Router Node

def router(state: MessagesState):
    """
    Router node.
    Is node ka kaam sirf state ko next routing function tak pahunchana hai.
    """
    return {}


# Decision Function

def route(state: MessagesState):
    question = state["messages"][-1].content.lower()

    if "+" in question:
        return "calculator"
    
    return "chatbot"

# Calculator Node
def calculator(state: MessagesState):
    return{
        "messages" : [
            AIMessage(content="Calculator Node Executed")
        ]
    }

# Chatbot Node
def chatbot(state: MessagesState):
    return {
        "messages" : [
            AIMessage(content="Chatbot Node Executed")
        ]
    }

# Create Graph
graph = StateGraph(MessagesState)

# Register Nodes
graph.add_node("router", router)
graph.add_node("calculator", calculator)
graph.add_node("chatbot" , chatbot)

# Edges
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router" , 
    route, 
    {
        "calculator": "calculator",

        "chatbot": "chatbot"
    }
)

graph.add_edge("calculator", END)
graph.add_edge("chatbot", END)

# Compile
app = graph.compile()

# RUN
results = app.invoke(
    {
        "messages" : [
            HumanMessage(content="2 + 2")
        ]
    }
)

for message in results["messages"]:
    print(f"{message.type} : {message.content}")