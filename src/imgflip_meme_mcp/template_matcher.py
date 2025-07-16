"""Template matching system for intelligent meme selection."""

import re
from typing import Dict, List, Optional, Any
from difflib import SequenceMatcher
from .imgflip_client import ImgflipClient


class TemplateMatcher:
    """Intelligent system for matching meme requests to templates."""
    
    def __init__(self):
        self.imgflip_client = ImgflipClient()
        self._template_aliases = {
            # Men's Warehouse meme
            "mens warehouse": ["181913649"],
            "men's warehouse": ["181913649"],
            "mens": ["181913649"],
            "guarantee": ["181913649"],
            "i guarantee it": ["181913649"],
            
            # Drake pointing/approving  
            "drake": ["112126428"],
            "drake pointing": ["112126428"],
            "drake approve": ["112126428"],
            "drake disapprove": ["112126428"],
            
            # Distracted boyfriend
            "distracted boyfriend": ["112126428"],
            "boyfriend looking back": ["112126428"],
            "cheating boyfriend": ["112126428"],
            
            # Popular memes
            "two buttons": ["87743020"],
            "expanding brain": ["112126428"],
            "woman yelling at cat": ["188390779"],
            "surprised pikachu": ["155067746"],
            "change my mind": ["129242436"],
            "this is fine": ["55311130"],
            "uno reverse": ["124055727"],
            "always has been": ["216951317"],
            
            # Classic memes
            "one does not simply": ["61579"],
            "most interesting man": ["61532"],
            "y u no": ["61527"],
            "philosoraptor": ["61516"],
            "success kid": ["61544"],
            "bad luck brian": ["61585"],
            "scumbag steve": ["61522"],
            "good guy greg": ["61520"],
            "first world problems": ["61539"],
            "overly attached girlfriend": ["61518"],
        }
    
    async def find_best_match(self, hint: str) -> Optional[Dict[str, Any]]:
        """Find the best matching template for a given hint."""
        hint_lower = hint.lower().strip()
        
        # Check direct aliases first
        for alias, template_ids in self._template_aliases.items():
            if alias in hint_lower or hint_lower in alias:
                # Get template details from cache
                templates = await self.imgflip_client.get_popular_templates()
                for template in templates:
                    if template["id"] in template_ids:
                        return template
        
        # If no direct match, search by similarity
        templates = await self.imgflip_client.get_popular_templates()
        if not templates:
            return None
        
        best_match = None
        best_score = 0.0
        
        for template in templates:
            score = self._calculate_similarity(hint_lower, template["name"].lower())
            if score > best_score and score > 0.3:  # Minimum similarity threshold
                best_score = score
                best_match = template
        
        return best_match
    
    def _calculate_similarity(self, hint: str, template_name: str) -> float:
        """Calculate similarity between hint and template name."""
        # Direct substring match gets high score
        if hint in template_name or template_name in hint:
            return 0.9
        
        # Use sequence matcher for fuzzy matching
        sequence_score = SequenceMatcher(None, hint, template_name).ratio()
        
        # Word-level matching
        hint_words = set(re.findall(r'\w+', hint.lower()))
        template_words = set(re.findall(r'\w+', template_name.lower()))
        
        if hint_words and template_words:
            word_score = len(hint_words & template_words) / len(hint_words | template_words)
        else:
            word_score = 0.0
        
        # Combine scores with weights
        return 0.6 * sequence_score + 0.4 * word_score
    
    async def search_templates(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for templates matching a query."""
        templates = await self.imgflip_client.search_templates(query)
        
        # Sort by similarity to query
        scored_templates = []
        for template in templates:
            score = self._calculate_similarity(query.lower(), template["name"].lower())
            scored_templates.append((score, template))
        
        # Sort by score (descending) and return top results
        scored_templates.sort(key=lambda x: x[0], reverse=True)
        return [template for _, template in scored_templates[:limit]]
    
    def get_template_suggestions(self) -> List[str]:
        """Get a list of supported template hints."""
        return list(self._template_aliases.keys())