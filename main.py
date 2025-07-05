#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import importlib.util

# Add the src directory to the path for local development
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def run_chatbot_with_json(input_json):
    """
    Run the chatbot using a JSON input (Python dict) and return the output as a dict.
    """
    # Patch the input/output handlers to use variables instead of files
    import src.input_handler as input_handler
    import src.output_handler as output_handler
    import src.workflow_setup as workflow_setup
    import src.model as model_mod

    # Patch load_conversation to use input_json
    def load_conversation_from_var(history_limit):
        return input_handler.load_conversation(history_limit, input_json=input_json)
    
    # Patch save_output_json to return output instead of writing to file
    output_result = {}
    def save_output_json_var(*args, **kwargs):
        # args: (None, result, summaries, output_json_path, previous_summaries, original_conversation)
        output_result['result'] = args[1]
        output_result['summaries'] = args[2]
        output_result['previous_summaries'] = args[4]
        output_result['original_conversation'] = args[5]
    
    # Monkey-patch the handlers
    input_handler.load_conversation = load_conversation_from_var
    output_handler.save_output_json = save_output_json_var

    # Run the logic from src/__init__.py
    init_spec = importlib.util.spec_from_file_location("src_init", src_path / "__init__.py")
    src_module = importlib.util.module_from_spec(init_spec)
    init_spec.loader.exec_module(src_module)
    return output_result

try:
    print("\U0001F504 Running chatbot ...")
    print("=" * 50)
    
    # Load and execute the src/__init__.py which contains the full implementation
    init_spec = importlib.util.spec_from_file_location("src_init", src_path / "__init__.py")
    src_module = importlib.util.module_from_spec(init_spec)
    
    # Execute the src module which will run the chatbot demo automatically
    init_spec.loader.exec_module(src_module)
    
    print("\n\U0001F389 Chatbot working successfully!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("   - Check if Ollama is running")
    print("   - Verify model is available: ollama list")
    print("   - Check dependencies: pip list")
