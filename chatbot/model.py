import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
# from langchain_core.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import START, MessagesState, StateGraph

def model_response(model, limit, state: MessagesState):
    system_prompt = (
        "You are a helpful assistant who is a sports nerd. "
        "You will be given a series of messages, and you should respond to the last message."
        "The provided chat history includes a summary of the earlier conversation."
    )

    system_message = SystemMessage(content=system_prompt)
    message_history = state["messages"][:-1]  # Exclude the last message
    
    if len(message_history) >= limit:
        last_messages = state["messages"][-1:]
        
        summary_prompt = (
            "Distill the above chat messages into a single summary message. "
            "Include as many specific details as you can."
        )
        summary_message = model.invoke(
            message_history + [HumanMessage(content=summary_prompt)]
        )
        
        # Delete messages that we no longer want to show up
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]]
        human_message = HumanMessage(content=last_messages.content)
        response = model.invoke(
            [system_message, summary_message, human_message]
        )
        
        message_updates = [summary_message, human_message, response] + delete_messages
    else:
        message_updates = model.invoke([system_message] + state["messages"])
        
    return {
        "messages": message_updates
    }