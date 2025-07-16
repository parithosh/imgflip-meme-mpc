# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that integrates with the Imgflip API to generate memes. The server exposes tools that allow LLMs to fetch meme templates and generate memes with custom text.

## Architecture

The server follows the standard MCP server architecture:
- **MCP Server**: Core server implementation using Python `mcp` library
- **Imgflip API Client**: HTTP client wrapper around Imgflip's REST API endpoints
- **Template Matcher**: Intelligent system for matching meme requests to templates
- **Transport Layer**: Stdio transport for integration with Claude

## Key Components

- **Server Setup**: Python MCP server with registered tools and stdio transport
- **API Integration**: HTTP client for Imgflip API calls with authentication and caching
- **Template Matching**: Advanced matching system with character recognition and fuzzy search
- **Input Validation**: Pydantic schemas for tool parameters and API responses

## Development Commands

This is a Python project with the following commands:
- `pip install -e .` - Install package in development mode
- `python test_mens_warehouse.py` - Test the Men's Warehouse meme example
- `python -m src.imgflip_meme_mcp.server` - Run the MCP server directly
- `black src/` - Format code
- `ruff check src/` - Lint code
- `pytest` - Run test suite (when tests are added)

## Configuration

The server requires Imgflip API credentials:
- Username and password for Imgflip account (free account works)
- Environment variables in `.env` file for API authentication
- Template caching configuration for performance

## MCP Integration

To use with Claude Code:
1. Install dependencies: `pip install -e .`
2. Configure credentials in `.env` file
3. Add to Claude's MCP configuration: `claude mcp add imgflip-meme-server imgflip-mcp`
4. Server runs via stdio transport when invoked by Claude

## API Endpoints Used

- `/get_memes` - Fetch popular meme templates (free tier)
- `/caption_image` - Generate memes with custom text (requires auth)
- `/search_memes` - Search meme templates (premium feature)