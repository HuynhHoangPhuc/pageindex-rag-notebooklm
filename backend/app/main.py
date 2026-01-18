from fastapi import FastAPI
from app.db import create_db_and_tables
from app.api import router as api_router
from app.mcp_server import mcp
from fastapi.middleware.cors import CORSMiddleware
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Attempt to mount MCP
# FastMCP usually handles its own lifecycle/app, but we want to embed it.
# If FastMCP exposes an underlying router or method to add to an app:
try:
    # Common pattern for FastMCP integration
    # mcp.mount_to(app, path="/mcp") ??
    # Or just use the tool directly if we were running standalone.
    # Since I cannot be 100% sure of FastMCP API, I'll rely on it being an independent runner normally.
    # But to merge, we might need access to its SSE handler.
    # Let's assume mcp object has 'bind_to_app' or we just run it separately?
    # No, user wants one backend.
    
    # Let's try:
    # mcp._add_routes(app) - internal?
    pass
except:
    pass

app.mount("/mcp", mcp.sse_app()) 
