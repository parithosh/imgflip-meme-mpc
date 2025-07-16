"""MCP server for intelligent meme generation using Imgflip API."""

import asyncio
import json
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

from .imgflip_client import ImgflipClient
from .template_matcher import TemplateMatcher


class MemeGenerationRequest(BaseModel):
    """Request model for meme generation."""
    template_hint: str
    top_text: str
    bottom_text: Optional[str] = None


class MemeSearchRequest(BaseModel):
    """Request model for meme template search."""
    query: str
    limit: Optional[int] = 10


app = Server("imgflip-meme-server")
imgflip_client = ImgflipClient()
template_matcher = TemplateMatcher()


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for meme generation."""
    return [
        Tool(
            name="generate_meme",
            description="Generate a meme using Imgflip API with intelligent template matching",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_hint": {
                        "type": "string",
                        "description": "A hint about which meme template to use (e.g., 'men's warehouse', 'distracted boyfriend', 'drake pointing')"
                    },
                    "top_text": {
                        "type": "string",
                        "description": "Text for the top of the meme"
                    },
                    "bottom_text": {
                        "type": "string",
                        "description": "Text for the bottom of the meme (optional for some templates)"
                    }
                },
                "required": ["template_hint", "top_text"]
            }
        ),
        Tool(
            name="search_meme_templates",
            description="Search for available meme templates",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for meme templates"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="list_popular_templates",
            description="List popular meme templates available on Imgflip",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of templates to return",
                        "default": 20
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for meme generation."""
    try:
        if name == "generate_meme":
            request = MemeGenerationRequest(**arguments)
            
            # Find the best matching template
            template = await template_matcher.find_best_match(request.template_hint)
            if not template:
                return [TextContent(
                    type="text",
                    text=f"Could not find a suitable meme template for '{request.template_hint}'. Try using search_meme_templates to find available templates."
                )]
            
            # Generate the meme
            result = await imgflip_client.generate_meme(
                template_id=template["id"],
                top_text=request.top_text,
                bottom_text=request.bottom_text or ""
            )
            
            if result["success"]:
                return [TextContent(
                    type="text",
                    text=f"Meme generated successfully!\n\nTemplate: {template['name']}\nURL: {result['data']['url']}\nPage URL: {result['data']['page_url']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to generate meme: {result.get('error_message', 'Unknown error')}"
                )]
        
        elif name == "search_meme_templates":
            request = MemeSearchRequest(**arguments)
            templates = await template_matcher.search_templates(request.query, request.limit)
            
            if templates:
                results = []
                for template in templates:
                    results.append(f"• {template['name']} (ID: {template['id']})")
                
                return [TextContent(
                    type="text",
                    text=f"Found {len(templates)} matching templates:\n\n" + "\n".join(results)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No templates found matching '{request.query}'"
                )]
        
        elif name == "list_popular_templates":
            limit = arguments.get("limit", 20)
            templates = await imgflip_client.get_popular_templates(limit)
            
            if templates:
                results = []
                for template in templates[:limit]:
                    results.append(f"• {template['name']} (ID: {template['id']})")
                
                return [TextContent(
                    type="text",
                    text=f"Popular meme templates:\n\n" + "\n".join(results)
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Could not retrieve popular templates"
                )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error calling tool {name}: {str(e)}"
        )]


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())