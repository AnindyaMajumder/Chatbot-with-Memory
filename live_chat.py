#!/usr/bin/env python3
"""
Live Chat Terminal Interface for the Chatbot with Memory.

This script provides a real-time interactive chat interface in the terminal.
No JSON files are generated - just direct conversation with the sports trainer chatbot.
"""

import sys
import os
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from datetime import datetime

# Add the src directory to the path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import chatbot components
from src.workflow_setup import create_workflow_app, create_model
from src.model import summarize_messages

class LiveChatbot:
    def __init__(self):
        """Initialize the live chatbot with memory."""
        self.app = create_workflow_app()
        self.model = create_model()
        self.conversation_history = []
        self.previous_summaries = []  # Store accumulated summaries like original implementation
        self.thread_id = "live_chat_session"
        self.history_limit = 20  # Same as original implementation
        
    def print_welcome(self):
        """Print welcome message and instructions."""
        print("=" * 60)
        print("🏋️  SPORTS TRAINER CHATBOT - LIVE CHAT")
        print("=" * 60)
        print("Hello! I'm your personal sports trainer assistant.")
        print("I can help you with:")
        print("  • Workout routines and exercise plans")
        print("  • Nutrition advice for athletes")
        print("  • Training tips and techniques")
        print("  • Sports performance optimization")
        print("  • Recovery and injury prevention")
        print("")
        print("💬 Start typing your questions!")
        print("🔄 Type 'quit', 'exit', or 'bye' to end the conversation")
        print("🗑️  Type 'clear' to reset conversation history")
        print("📊 Type 'memory' to see memory statistics")
        print("=" * 60)
        print("")

    def manage_conversation_history(self):
        """
        Manage conversation history following the original memory implementation.
        Creates chunks, summarizes them, and maintains the proper message structure.
        """
        if len(self.conversation_history) > self.history_limit:
            # Calculate how many messages need to be summarized
            messages_to_summarize = self.conversation_history[:-self.history_limit]
            recent_messages = self.conversation_history[-self.history_limit:]
            
            # Create chunks following original implementation logic
            summary_chunks = []
            chunk = []
            for message in messages_to_summarize:
                chunk.append(message)
                if len(chunk) >= self.history_limit:
                    summary_chunks.append(chunk)
                    chunk = []
            
            # Handle remaining messages in partial chunk
            if chunk:
                summary_chunks.append(chunk)
            
            # Summarize chunks using the original summarize_messages function
            if summary_chunks:
                new_summaries = summarize_messages(self.model, summary_chunks)
                # Add new summaries to previous summaries (accumulate like original)
                self.previous_summaries.extend(new_summaries)
            
            # Update conversation history to keep only recent messages
            self.conversation_history = recent_messages
    
    def build_message_history_for_model(self):
        """
        Build the complete message history following original implementation:
        [all previous summaries] + [new summaries] + [recent unsummarized messages]
        """
        complete_history = []
        
        # Add all previous summaries first
        for summary in self.previous_summaries:
            complete_history.append(summary)
        
        # Add current conversation history (recent messages)
        complete_history.extend(self.conversation_history)
        
        return complete_history
    
    def show_memory_stats(self):
        """Display current memory statistics."""
        total_summaries = len(self.previous_summaries)
        current_messages = len(self.conversation_history)
        summarized_message_count = total_summaries * self.history_limit
        
        print("\n📊 MEMORY STATISTICS")
        print("=" * 30)
        print(f"📝 Active summaries: {total_summaries}")
        print(f"💬 Current messages: {current_messages}")
        print(f"🗂️  Summarized messages: {summarized_message_count}")
        print(f"📊 Total memory span: {summarized_message_count + current_messages} messages")
        print(f"🎯 History limit: {self.history_limit}")
        print("=" * 30)
        print("")

    def chat_loop(self):
        """Main chat loop for live conversation."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for chatting! Keep training hard!")
                    break
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    self.previous_summaries = []  # Also clear accumulated summaries
                    print("\n🗑️  Conversation history and summaries cleared!")
                    print("=" * 40)
                    continue
                elif user_input.lower() == 'memory':
                    self.show_memory_stats()
                    continue
                elif not user_input:
                    continue
                
                # Add user message to history
                user_message = HumanMessage(content=user_input)
                self.conversation_history.append(user_message)
                
                # Manage history length
                self.manage_conversation_history()
                
                # Show thinking indicator
                print("\n🤔 Thinking...", end="", flush=True)
                
                # Build complete message history following original implementation
                complete_message_history = self.build_message_history_for_model()
                
                # Get bot response using complete history
                result = self.app.invoke(
                    {"messages": complete_message_history},
                    config={"configurable": {"thread_id": self.thread_id}}
                )
                
                # Clear thinking indicator
                print("\r" + " " * 15 + "\r", end="")
                
                # Extract and display bot response
                bot_response = result["messages"][-1]
                print(f"🏋️  Trainer: {bot_response.content}")
                print("-" * 50)
                
                # Add bot response to history
                self.conversation_history.append(bot_response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error occurred: {str(e)}")
                print("🔄 Let's try again...")
                continue

if __name__ == "__main__":
    """Main function to start the live chat."""
    try:
        chatbot = LiveChatbot()
        chatbot.chat_loop()
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Check if Ollama is running: ollama serve")
        print("   - Verify model is available: ollama list")
        print("   - Check dependencies: pip install -r requirements.txt")
        sys.exit(1)

