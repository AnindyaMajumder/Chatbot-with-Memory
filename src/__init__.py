import os
from langchain_core.messages import AIMessage, HumanMessage
from src.input_handler import load_conversation
from src.workflow_setup import create_workflow_app, create_model
from src.model import summarize_messages
from src.output_handler import save_output_json
from tests.test_var import load_input_json

history_limit = 20 # Ideal for 8B params 

# Use the input handler to load messages 
input_messages, summary_chunks, total_messages, previous_summaries = load_conversation(history_limit)

# Summarize the summary_chunks using the model
model = create_model()
summaries = summarize_messages(model, summary_chunks)

# Build the new message history: [all previous summaries] + [new summaries] + [unsummarized texts]
message_history = []
for summary in previous_summaries:
    message_history.append(summary)
for summary in summaries:
    message_history.append(summary)
message_history += input_messages[-total_messages:]

# Create the workflow app
app = create_workflow_app()
result = app.invoke(
    {
        "messages": message_history,
    },
    config={"configurable": {"thread_id": "4"}}
)

# Save output to output.json
original_conversation = load_input_json()
output_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'output.json')
save_output_json(None, result, summaries, output_json_path, previous_summaries, original_conversation)
