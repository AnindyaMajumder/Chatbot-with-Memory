import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from model import model_response
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Will remove later
demo_ephemeral_chat_history = [
    HumanMessage(content="Hey there! I'm Nemo."),
    AIMessage(content="Hello!"),
    HumanMessage(content="How are you today?"),
    AIMessage(content="Fine thanks!"),
]
# __________________________________________________________

history_limit = 5
workflow = StateGraph(state_schema=MessagesState)
model = OllamaLLM(model="llama3.1:8b")

def model_node(state):
    return model_response(model, history_limit, state)

workflow.add_node("model", model_node)
workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
result = app.invoke(
    {
        "messages": demo_ephemeral_chat_history 
        + [HumanMessage("What did I say?")],
    },
    config={"configurable": {"thread_id": "4"}}
)

print("Current chat:")
for message in result["messages"]:
    if hasattr(message, 'type'):
        print(f"{message.type}: {message.content}")
    else:
        print(f"{type(message).__name__}: {message.content}")