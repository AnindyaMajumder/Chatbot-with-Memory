from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
# from langchain_core.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import START, MessagesState, StateGraph

def model_response(model, limit, state: MessagesState):
    system_prompt = (
        "You are a helpful assistant who is a sports trainer. "
        "You will be given a series of messages, and you should respond to the last message."
        "The provided chat history includes a summary of the earlier conversation."
    )

    system_message = SystemMessage(content=system_prompt)
    messages = state["messages"]
    overlap = 10  # Number of messages to overlap between summaries
    summary_info = None

    if len(messages) > 0 and len(messages) % limit == 0:
        # Periodic summarization every 'limit' messages (e.g., 50)
        to_summarize = messages[:-overlap]
        overlap_messages = messages[-overlap:]
        last_message = messages[-1]

        summary_prompt = (
            "Distill the above chat messages into a single summary message. "
            "Include as many specific details as you can."
        )
        summary_message = model.invoke(
            to_summarize + [HumanMessage(content=summary_prompt)]
        )

        # Prepare summary info to be saved externally
        summary_info = {
            "summary_index": len(messages),
            "summary": summary_message.content
        }

        new_context = [summary_message] + overlap_messages + [last_message]
        response = model.invoke([system_message] + new_context)
        message_updates = [summary_message] + overlap_messages + [last_message, response]
    else:
        response = model.invoke([system_message] + messages)
        message_updates = [response]

    return {
        "messages": message_updates,
        "summary_info": summary_info
    }