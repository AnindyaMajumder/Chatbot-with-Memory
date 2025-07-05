from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from src.model import model_response


def create_model():
    """Create and configure the OllamaLLM model."""
    return OllamaLLM(
        model="qwen3:0.6b", 
        temperature=0.5, 
        max_tokens=512, 
        top_p=0.9, 
        top_k=40,
        stop=["<|endoftext|>"]
    )


def create_workflow_app():
    """Create and compile the workflow application with memory."""
    workflow = StateGraph(state_schema=MessagesState)
    model = create_model()
    
    def model_node(state):
        return model_response(model, state)
    
    workflow.add_node("model", model_node)
    workflow.add_edge(START, "model")
    
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app
