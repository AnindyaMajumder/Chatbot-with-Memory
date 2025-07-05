from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState


def model_response(model, state: MessagesState):
    system_prompt = (
        "You are a helpful assistant who is a sports trainer. "
        "You will be given a series of messages, and you should respond to the last message."
        "The provided chat history includes a summary of the earlier conversation."
    )

    system_message = SystemMessage(content=system_prompt)
    messages = state["messages"]
    response = model.invoke([system_message] + messages)
    return {
        "messages": [response],
        "summary_info": None
    }

def summarize_messages(model, message_chunks):
    """Summarize each chunk of messages using the model."""
    summaries = []
    for chunk in message_chunks:
        if not chunk:
            continue
        summary_prompt = "Distill the above chat messages into a single summary message. Include as many specific details as you can."
        summary_message = model.invoke(chunk + [HumanMessage(content=summary_prompt)])
        summaries.append(summary_message)
    return summaries