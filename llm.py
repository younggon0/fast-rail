import os
from langchain_anthropic import ChatAnthropic

def init_llm():
    """Initialize Anthropic LLM via LangChain"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        api_key=api_key,
        temperature=0.7
    )

def test_connection():
    """Test LLM connection and return status"""
    try:
        llm = init_llm()
        response = llm.invoke("Hello")
        return {"success": True, "message": "Connected"}
    except Exception as e:
        return {"success": False, "error": str(e)}