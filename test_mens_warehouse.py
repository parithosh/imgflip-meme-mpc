#!/usr/bin/env python3
"""Test script for Men's Warehouse meme generation."""

import asyncio
import os
from src.imgflip_meme_mcp.imgflip_client import ImgflipClient
from src.imgflip_meme_mcp.template_matcher import TemplateMatcher


async def test_mens_warehouse_meme():
    """Test generating a Men's Warehouse 'I guarantee it' meme."""
    print("🧪 Testing Men's Warehouse meme generation...")
    
    # Check if credentials are set
    if not os.getenv("IMGFLIP_USERNAME") or not os.getenv("IMGFLIP_PASSWORD"):
        print("❌ Error: Imgflip credentials not found!")
        print("Please create a .env file with:")
        print("IMGFLIP_USERNAME=your_username")
        print("IMGFLIP_PASSWORD=your_password")
        print("\nYou can get free credentials at: https://imgflip.com/signup")
        return
    
    client = ImgflipClient()
    matcher = TemplateMatcher()
    
    # Test template fetching
    print("📥 Fetching popular templates...")
    templates = await client.get_popular_templates(20)
    print(f"✅ Found {len(templates)} templates")
    
    # Test template matching
    print("\n🔍 Testing template matching for 'men's warehouse'...")
    template = await matcher.find_best_match("men's warehouse")
    
    if template:
        print(f"✅ Found template: {template['name']} (ID: {template['id']})")
        
        # Test meme generation
        print("\n🎨 Generating meme...")
        result = await client.generate_meme(
            template_id=template["id"],
            top_text="Claude will nail this meme",
            bottom_text="I guarantee it"
        )
        
        if result["success"]:
            print(f"🎉 Meme generated successfully!")
            print(f"URL: {result['data']['url']}")
            print(f"Page: {result['data']['page_url']}")
        else:
            print(f"❌ Meme generation failed: {result.get('error_message', 'Unknown error')}")
    else:
        print("❌ Could not find Men's Warehouse template")
        
        # Show available templates for debugging
        print("\n📋 Available templates:")
        for i, t in enumerate(templates[:10]):
            print(f"  {i+1}. {t['name']} (ID: {t['id']})")


async def test_search_functionality():
    """Test the search functionality."""
    print("\n🔍 Testing search functionality...")
    
    matcher = TemplateMatcher()
    
    search_terms = ["guarantee", "warehouse", "drake", "distracted"]
    
    for term in search_terms:
        print(f"\n  Searching for '{term}'...")
        results = await matcher.search_templates(term, 3)
        
        if results:
            for i, template in enumerate(results):
                print(f"    {i+1}. {template['name']} (ID: {template['id']})")
        else:
            print(f"    No results found for '{term}'")


if __name__ == "__main__":
    asyncio.run(test_mens_warehouse_meme())
    asyncio.run(test_search_functionality())