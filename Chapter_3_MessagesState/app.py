from langgraph.graph import StateGraph 
from langgraph.graph import MessagesState

from langchain_core.messages import AIMessage


# Node
def chatbot(state: MessagesState):
    return {
        "messages" : [
            AIMessage(content="Hello from LangGraph")
        ]
    }

# Graph
graph = StateGraph(MessagesState)

# Add Node
graph.add_node("chatbot",chatbot)

# Entry Point
graph.set_entry_point("chatbot")

# Finish Point
graph.set_finish_point("chatbot")

# Compile
app = graph.compile()

# RUN
result = app.invoke(
    {
        "messages" : []
    }
)

print(result)

