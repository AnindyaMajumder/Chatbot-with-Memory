import json
import os
import re

def strip_think_sections(text):
    """Remove <think>...</think> sections from a string."""
    return re.sub(r'<think>[\s\S]*?</think>\s*', '', text, flags=re.IGNORECASE)

def save_output_json(input_json_path, result, summaries, output_json_path, existing_summaries=None, conversation_data=None):
    """
    Save the output JSON as a flat list: first object is the summary, followed by all conversation messages (with appended AI response if present), and remove any existing summary objects.
    Appends new summaries to the existing summary array.
    Also returns a variable containing the same JSON structure as written to file.
    """
    # 1. Load the original input JSON or use provided conversation data
    if input_json_path is not None:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            input_conversation = json.load(f)
        
        # Extract existing summary array if present
        extracted_summaries = []
        for obj in input_conversation:
            if isinstance(obj, dict) and 'summary' in obj:
                if isinstance(obj['summary'], list):
                    extracted_summaries.extend(obj['summary'])
        existing_summaries = extracted_summaries if existing_summaries is None else existing_summaries
    else:
        # Use provided conversation_data and existing_summaries
        input_conversation = conversation_data or []
        existing_summaries = existing_summaries or []

    # Remove any existing summary objects (objects with only a 'summary' key)
    filtered_conversation = [obj for obj in input_conversation if not (isinstance(obj, dict) and list(obj.keys()) == ["summary"])]

    # 2. Get the latest AI response from the model result
    latest_ai_response = None
    if isinstance(result, dict) and 'messages' in result and result['messages']:
        last_message = result['messages'][-1]
        if hasattr(last_message, 'content'):
            latest_ai_response = last_message.content
        elif isinstance(last_message, dict) and 'content' in last_message:
            latest_ai_response = last_message['content']

    # 3. Prepare the output conversation list (copy all input, append new AI response if present)
    output_conversation = filtered_conversation.copy()
    if latest_ai_response:
        output_conversation.append({
            "role": "ai",
            "content": latest_ai_response
        })

    # 4. Prepare the summary as the first object, handling empty string replacement
    new_summaries = []
    if isinstance(summaries, list):
        new_summaries = [strip_think_sections(msg.content) if hasattr(msg, 'content') else strip_think_sections(str(msg)) for msg in summaries]
    elif isinstance(summaries, str):
        new_summaries = [summaries]
    
    # Check if existing summaries contain only empty strings and replace them with first real summary
    if existing_summaries == [""] and new_summaries:
        # Replace the empty string with the first new summary
        combined_summaries = new_summaries
    else:
        # Append new summaries to existing (normal case)
        combined_summaries = existing_summaries + new_summaries
    summary_obj = {"summary": combined_summaries}

    # 5. Write output: summary first, then conversation
    output_json_variable = [summary_obj] + output_conversation
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_json_variable, f, indent=4, ensure_ascii=False)
    return output_json_variable
