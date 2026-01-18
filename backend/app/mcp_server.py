from mcp.server.fastmcp import FastMCP
from app.rag import rag_client
from app.db import get_session, Document, User
from sqlmodel import select

# Initialize FastMCP
mcp = FastMCP("PageIndexRAG")

@mcp.tool()
def query_knowledge_base(query: str, doc_ids: list[str]) -> str:
    """Query the PageIndex RAG system with a specific question and document IDs."""
    try:
        response = rag_client.query(query, doc_ids)
        if hasattr(response, 'choices') and response.choices:
             return response.choices[0].message.content
        return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_available_documents(user_email: str) -> str:
    """List documents available for a specific user email."""
    # We need to create a new session here since we are not in a request context
    from app.db import engine
    from sqlmodel import Session
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == user_email)).first()
        if not user:
            return "User not found"
        docs = session.exec(select(Document).where(Document.user_id == user.id)).all()
        return "\n".join([f"ID: {d.pageindex_file_id}, Name: {d.filename}" for d in docs])

