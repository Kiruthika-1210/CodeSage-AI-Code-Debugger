from fastapi import APIRouter
from models.analyze_request import AnalyzeRequest
from services.analyze_service import analyze_full

router = APIRouter(prefix = "/analyze",
                   tags = ['Analyze'])

@router.post("")
def analyze_code(request: AnalyzeRequest):
    return analyze_full(request.code)


