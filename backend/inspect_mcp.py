try:
    import mcp
    print("mcp package found.")
    print(dir(mcp))
    import mcp.server
    print("mcp.server found.")
    print(dir(mcp.server))
except ImportError as e:
    print(f"ImportError: {e}")
