import json
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from src.model import model_response
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from src.input_handler import load_conversation

# Use the input handler to load messages
input_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'input.json')
input_messages = load_conversation(input_json_path)

history_limit = 100 # Ideal for 8B params 
workflow = StateGraph(state_schema=MessagesState)
model = OllamaLLM(model="llama3.1:8b", 
                  temperature=0.5, 
                  max_tokens=512, 
                  top_p=0.9, 
                  top_k=40,
                  stop=["<|endoftext|>"]
                )

def model_node(state):
    return model_response(model, history_limit, state)

workflow.add_node("model", model_node)
workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
result = app.invoke(
    {
        "messages": input_messages,
    },
    config={"configurable": {"thread_id": "4"}}
)

# Save output to output.json
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'output.json')
output_data = []
for i, message in enumerate(result["messages"]):
    if i == len(result["messages"]) - 1 or isinstance(message, AIMessage):
        role = "ai"
    elif isinstance(message, HumanMessage):
        role = "human"
    else:
        role = type(message).__name__
    output_data.append({"role": role, "content": message.content})

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)