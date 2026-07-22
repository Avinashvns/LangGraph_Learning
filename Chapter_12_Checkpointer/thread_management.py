from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)

from langgraph.checkpoint.memory import InMemorySaver

from langchain_ollama import ChatOllama

# LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# Node
def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])

    return { "messages" : [response]}

# Create Graph
builder = StateGraph(MessagesState)

# Register node
builder.add_node("chatbot",chatbot)

# Edges
builder.add_edge(START , "chatbot")
builder.add_edge("chatbot" , END)

# Memory
memory = InMemorySaver()

# Compile
graph = builder.compile(checkpointer=memory)

# Chat Loop
while True:

    thread = input("\nThread ID :")

    if thread.lower() == "exit":
        break

    question = input("You :")
    config = {
        "configurable" : {
            "thread_id" : thread
        }
    }

    result = graph.invoke(
        {
            "messages" : [
                {
                    "role" : "user",
                    "content" : question
                }
            ]
        },
        config=config
    )

    print(
            "\nAI :",
            result["messages"][-1].content
        )
  