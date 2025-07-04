#!/usr/bin/env python3
"""
Main entry point for the chatbot with memory.

This script demonstrates the chatbot functionality with conversation memory,
message history management, and sports-focused assistant personality.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path for local development
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    # Execute the complete implementation from src
    import importlib.util
    
    print("🔄 Running chatbot ...")
    print("=" * 50)
    
    # Load and execute the src/__init__.py which contains the full implementation
    init_spec = importlib.util.spec_from_file_location("src_init", src_path / "__init__.py")
    src_module = importlib.util.module_from_spec(init_spec)
    
    # Execute the src module which will run the chatbot demo automatically
    init_spec.loader.exec_module(src_module)
    
    print("\n🎉 Chatbot working successfully!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("   - Check if Ollama is running")
    print("   - Verify model is available: ollama list")
    print("   - Check dependencies: pip list")
