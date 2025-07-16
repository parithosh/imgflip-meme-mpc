"""Imgflip API client for meme generation."""

import os
import asyncio
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

load_dotenv()


class ImgflipClient:
    """Client for interacting with the Imgflip API."""
    
    BASE_URL = "https://api.imgflip.com"
    
    def __init__(self):
        self.username = os.getenv("IMGFLIP_USERNAME")
        self.password = os.getenv("IMGFLIP_PASSWORD")
        self._template_cache = None
    
    async def get_popular_templates(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get popular meme templates from Imgflip."""
        if self._template_cache is None:
            await self._fetch_templates()
        
        templates = self._template_cache or []
        if limit:
            templates = templates[:limit]
        
        return templates
    
    async def _fetch_templates(self) -> None:
        """Fetch templates from Imgflip API and cache them."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(f"{self.BASE_URL}/get_memes", timeout=10)
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("success"):
                self._template_cache = data["data"]["memes"]
            else:
                self._template_cache = []
        except Exception as e:
            print(f"Error fetching templates: {e}")
            self._template_cache = []
    
    async def generate_meme(self, template_id: str, top_text: str, bottom_text: str = "") -> Dict[str, Any]:
        """Generate a meme using the Imgflip API."""
        if not self.username or not self.password:
            return {
                "success": False,
                "error_message": "Imgflip credentials not configured. Please set IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables."
            }
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    f"{self.BASE_URL}/caption_image",
                    data={
                        "template_id": template_id,
                        "username": self.username,
                        "password": self.password,
                        "text0": top_text,
                        "text1": bottom_text
                    },
                    timeout=30
                )
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error_message": "Request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error_message": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error_message": f"Unexpected error: {str(e)}"
            }
    
    async def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """Search for templates by name (basic implementation)."""
        if self._template_cache is None:
            await self._fetch_templates()
        
        if not self._template_cache:
            return []
        
        query_lower = query.lower()
        matching_templates = []
        
        for template in self._template_cache:
            if query_lower in template["name"].lower():
                matching_templates.append(template)
        
        return matching_templates
    
    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by ID."""
        if not self._template_cache:
            return None
        
        for template in self._template_cache:
            if template["id"] == template_id:
                return template
        
        return None