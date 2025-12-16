from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyzeResponse(BaseModel):
    issues : List[Dict[str, Any]]
    complexity : Dict[str, Any]
    qualityScore : int