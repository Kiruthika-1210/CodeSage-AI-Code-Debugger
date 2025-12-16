from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AIRequest(BaseModel):
    code: str
    issues: Optional[List[Dict[str, Any]]] = None
    complexity: Optional[Dict[str, Any]] = None
    quality: Optional[Dict[str, Any]] = None
