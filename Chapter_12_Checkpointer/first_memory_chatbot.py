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

# Chatbot Node

def chatbot(state: MessagesState):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

# Graph

builder = StateGraph(MessagesState)

# Register Node

builder.add_node(
    "chatbot",
    chatbot
)

# Create Edges

builder.add_edge(
    START,
    "chatbot"
)

builder.add_edge(
    "chatbot",
    END
)


# Memory
memory = InMemorySaver()

# Compile
graph = builder.compile(
    checkpointer=memory
)

# Thread
config = {
    "configurable" : {
        "thread_id" : "user_1"
    }
}

# Chat loop
while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config=config
    )

    print(
        "\nAI :",
        result["messages"][-1].content
    )