import json
from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Tuple
from tests.test_var import load_input_json

def load_conversation(history_limit=5) -> Tuple[List, List[List], int, list]:
    conversation = load_input_json()

    # Extract existing summaries (if any)
    existing_summaries = []
    for obj in conversation:
        if isinstance(obj, dict) and 'summary' in obj and isinstance(obj['summary'], list):
            existing_summaries = obj['summary']
            break

    num_existing_summaries = len(existing_summaries)
    summarized_texts = num_existing_summaries * history_limit

    # Only process conversation after already summarized texts
    conversation_to_summarize = [entry for entry in conversation if not (isinstance(entry, dict) and 'summary' in entry)]
    unsummarized = conversation_to_summarize[summarized_texts:]

    # Prepare summary_chunks
    summary_chunks = []
    messages = []
    count = 0
    for entry in unsummarized:
        if 'role' not in entry or entry['role'] not in ['human', 'ai']:
            continue
        messages.append(HumanMessage(content=entry['content'])) if entry['role'] == 'human' else messages.append(AIMessage(content=entry['content']))
        count += 1
        if count % history_limit == 0:
            summary_chunks.append(messages)
            messages = []
    # Any leftover messages (not enough for a full chunk) go to remaining_messages
    remaining_messages = messages
    count_remaining = len(remaining_messages)

    return remaining_messages, summary_chunks, count_remaining, existing_summaries