from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
from mcp_server.tools import list_tools_handler, call_tool_handler

server = Server("knowledge-base-server")

@server.list_tools()
async def handle_list_tools():
    return await list_tools_handler()

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    return await call_tool_handler(name, arguments)

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())