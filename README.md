# Imgflip Meme MCP Server

A Model Context Protocol (MCP) server that enables Claude to generate memes using the Imgflip API with intelligent template matching.

![Example Meme](https://i.imgflip.com/a0eaov.jpg)

## Features

- 🎯 **Intelligent Template Matching**: Automatically finds the best meme template based on your description
- 🔍 **Template Search**: Search through available meme templates 
- 🎨 **Meme Generation**: Create custom memes with your text
- 🧠 **Smart Aliases**: Built-in recognition for popular memes like "Men's Warehouse", "Drake pointing", etc.

## Quick Start

### 1. Installation

```bash
# Clone and install
git clone <your-repo-url>
cd imgflip-meme-mcp
python3 -m venv venv
source venv/bin/activate
uv pip install -e .
```

### 2. Get Imgflip Credentials

1. Sign up for a free account at [imgflip.com](https://imgflip.com/signup)
2. Copy `.env.example` to `.env`
3. Add your credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Test the Implementation

```bash
# Test Men's Warehouse meme generation
python test_mens_warehouse.py
```

### 4. Configure with Claude

Add to your Claude MCP configuration:

```json
{
  "mcpServers": {
    "imgflip-meme": {
      "command": "uv",
      "args": ["run", "-m", "imgflip_meme_mcp.server"],
      "cwd": "/path/to/imgflip-meme-mcp"
    }
  }
}
```

## Usage Examples

Once configured with Claude, you can generate memes like:

```
Create a meme "Claude will nail this meme", "I guarantee it"
```

This will automatically:
1. Recognize "I guarantee it" as the Men's Warehouse meme
2. Find the correct template
3. Generate the meme with your custom text
4. Return the URL to your generated meme

## Supported Templates

The system includes smart recognition for popular memes:

- **Men's Warehouse**: "guarantee", "mens warehouse", "I guarantee it"
- **Drake Pointing**: "drake", "drake pointing", "approve/disapprove"
- **Distracted Boyfriend**: "distracted boyfriend", "cheating boyfriend"
- **Two Buttons**: "two buttons", "choice"
- **And many more...**

## API Tools

The MCP server exposes these tools to Claude:

- `generate_meme`: Create a meme with intelligent template matching
- `search_meme_templates`: Search for available templates
- `list_popular_templates`: List popular meme templates

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Format code
black src/

# Lint code  
ruff check src/

# Run tests
python test_mens_warehouse.py
```

## Architecture

- **MCP Server**: Core server using Python `mcp` library
- **Imgflip Client**: HTTP client for Imgflip API
- **Template Matcher**: Intelligent template selection system
- **Environment Config**: Secure credential management

## License

MIT License - see LICENSE file for details.