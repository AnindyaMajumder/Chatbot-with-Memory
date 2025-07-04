import json
from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Tuple

def load_conversation(json_path: str) -> List:
    with open(json_path, 'r', encoding='utf-8') as f:
        conversation = json.load(f)

    messages = []
    for entry in conversation:
        if entry['role'] == 'human':
            messages.append(HumanMessage(content=entry['content']))
        elif entry['role'] == 'ai':
            messages.append(AIMessage(content=entry['content']))

    history = []
    last_human = None
    for i, msg in enumerate(messages):
        if isinstance(msg, HumanMessage):
            if i == len(messages) - 1:
                last_human = msg
                break
        history.append(msg)

    input_messages = history + [last_human] if last_human else history
    return input_messages
