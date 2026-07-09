from pydantic import BaseModel
from typing import Optional, List

class PostCreate(BaseModel):
    subject: str
    description: Optional[str] = None
    tags: List[str] = []            # or Optional[str] if you store as comma‑separated
    image_url: Optional[str] = None
    content: str


class PostHandler:
    def jsonEncode(self, data): 
        return {
            "title": data['title'],
            "content": data['content']
        }