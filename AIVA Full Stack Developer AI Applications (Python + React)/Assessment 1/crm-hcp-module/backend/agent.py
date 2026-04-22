"""LangGraph workflow and ChatGroq setup for CRM-HCP module"""
from typing import Any, Dict, Optional
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize ChatGroq
def setup_chat_groq():
    """Initialize ChatGroq with API key"""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    chat = ChatGroq(
        temperature=0,
        groq_api_key=groq_api_key,
        model_name="gemma2-9b-it"  # Primary model for efficiency
    )
    return chat


# Initialize the LLM
llm = None

def initialize_agent():
    """Initialize the LangGraph agent"""
    global llm
    try:
        llm = setup_chat_groq()
        print("ChatGroq initialized successfully")
    except Exception as e:
        print(f"Error initializing ChatGroq: {e}")
        raise


# LangGraph workflow state
class AgentState(dict):
    """State management for LangGraph workflow"""
    def __init__(self):
        super().__init__()
        self['messages'] = []
        self['conversation_id'] = None
        self['user_id'] = None
        self['context'] = {}
        self['tool_results'] = {}


# Process user message through the agent
async def process_message(user_id: str, message: str, conversation_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process user message through the LangGraph agent.
    
    Args:
        user_id: User identifier
        message: User's message
        conversation_id: Optional conversation ID for multi-turn
        context: Optional context data
        
    Returns:
        Dictionary with agent response and metadata
    """
    if llm is None:
        initialize_agent()
    
    state = AgentState()
    state['user_id'] = user_id
    state['conversation_id'] = conversation_id or f"conv_{user_id}_{int(os.times()[4]*1000)}"
    state['messages'].append({"role": "user", "content": message})
    state['context'] = context or {}
    
    # Process message with LLM
    try:
        response = llm.invoke([{"role": "user", "content": message}])
        agent_response = response.content
        
        return {
            "conversation_id": state['conversation_id'],
            "response": agent_response,
            "status": "success",
            "metadata": {
                "user_id": user_id,
                "messages_count": len(state['messages'])
            }
        }
    except Exception as e:
        return {
            "conversation_id": state['conversation_id'],
            "response": f"Error processing message: {str(e)}",
            "status": "error",
            "metadata": {"error": str(e)}
        }


# Define tools for the agent
def get_agent_tools():
    """Get the list of tools available to the agent"""
    from tools import TOOLS
    return TOOLS


# Initialize on module load
def on_module_init():
    """Initialize agent on module load"""
    try:
        initialize_agent()
    except Exception as e:
        print(f"Warning: Could not initialize agent on startup: {e}")


# Call initialization
on_module_init()

import os
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from tools import (
    log_interaction, 
    edit_interaction, 
    summarize_voice_note, 
    generate_suggested_followups, 
    query_hcp_history
)
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq LLM (Ensure GROQ_API_KEY is in your .env file)
llm = ChatGroq(
    model="gemma2-9b-it", 
    temperature=0, 
    max_retries=2
)

# Bind the 5 required tools
tools = [
    log_interaction,
    edit_interaction,
    summarize_voice_note,
    generate_suggested_followups,
    query_hcp_history
]

# Create the LangGraph Agent
# Using prebuilt react_agent for seamless tool calling and message state routing
agent_executor = create_react_agent(llm, tools)