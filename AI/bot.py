from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from AI.universal_tools import universal_tools
from AI.rag import make_query_rag_tool
from functools import partial
from langchain.tools import tool

llm = ChatGroq(model="moonshotai/kimi-k2-instruct-0905", temperature=0.2)

system_prompt = SystemMessage(
    content="""You are a helpful and knowledgeable AI assistant with access to real-time web search and the user's personal knowledge base.

Guidelines:
- Provide clear, concise answers without unnecessary jargon
- When you search the web, always cite your sources with URLs
- If information comes from the user's documents, mention that it's from their knowledge base
- If you're unsure, admit it rather than making up information
- Be conversational and friendly while staying professional

When to use your tools:
- Use web search for current events, facts, and general knowledge
- Use the knowledge base for information specific to the user's documents and past conversations
- Use date/time tool when temporal context matters

Always prioritize accuracy and cite your sources when making factual claims."""
)

async def get_ai_response(
    user_message: str,
    conversation_id: int,
    chat_history: list  # List of HumanMessage/AIMessage objects
) -> str:
    """Get AI response with tools"""
    
    # Create RAG tools for this conversation
    query = make_query_rag_tool(conversation_id=conversation_id)
    
    # Combine all tools
    all_tools = universal_tools + [query]
    
    # Create agent
    agent = create_agent(model=llm, tools=all_tools)
    
    # Build full message history
    full_history = [system_prompt] + chat_history + [HumanMessage(content=user_message)]
    
    # Get AI response
    config = {"recursion_limit": 10}
    
    try:
        response = await agent.ainvoke({"messages": full_history}, config=config)
        ai_message_content = response["messages"][-1].content
        return ai_message_content
    except Exception as e:
        return f"I encountered an error: {str(e)}"