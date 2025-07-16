#!/usr/bin/env python3
"""Setup script for Imgflip Meme MCP Server."""

import os
import sys

def setup_env():
    """Set up environment file with credentials."""
    print("🔧 Imgflip Meme MCP Server Setup")
    print("=" * 40)
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return
    
    print("\n📝 Setting up Imgflip credentials...")
    print("You need a free Imgflip account from: https://imgflip.com/signup")
    
    username = input("\nEnter your Imgflip username: ").strip()
    password = input("Enter your Imgflip password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required!")
        sys.exit(1)
    
    with open(".env", "w") as f:
        f.write(f"# Imgflip API Credentials\n")
        f.write(f"IMGFLIP_USERNAME={username}\n")
        f.write(f"IMGFLIP_PASSWORD={password}\n")
    
    print("✅ .env file created successfully!")
    print("\n🧪 Run 'python test_mens_warehouse.py' to test the setup")

def show_usage():
    """Show usage instructions."""
    print("\n🎯 How to use with Claude:")
    print("1. Add this to your Claude MCP config:")
    print(f"""
{{
  "mcpServers": {{
    "imgflip-meme": {{
      "command": "python",
      "args": ["-m", "imgflip_meme_mcp.server"],
      "cwd": "{os.getcwd()}"
    }}
  }}
}}
""")
    print("2. Then say to Claude: 'Create a meme with \"My text\", \"Bottom text\"'")

if __name__ == "__main__":
    setup_env()
    show_usage()