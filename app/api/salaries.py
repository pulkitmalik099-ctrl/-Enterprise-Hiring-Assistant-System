from fastapi import APIRouter

router = APIRouter(prefix="/api/salaries", tags=["Salaries"])

@router.post("/{candidate_id}/research/{job_id}")
async def research_salary(candidate_id: str, job_id: str):
    """Research market salary"""
    return {"recommended_salary": 160000, "range": {"min": 140000, "max": 200000}}

@router.get("/research/{research_id}")
async def get_research(research_id: str):
    """Get salary research"""
    return {"research_id": research_id, "salary": 160000}

@router.post("/{candidate_id}/evaluate-offer/{job_id}")
async def evaluate_offer(candidate_id: str, job_id: str, offer: dict):
    """Evaluate offer"""
    return {"offer_score": 82, "recommendation": "Good offer"}

@router.get("/{candidate_id}/offer-evaluation/{eval_id}")
async def get_evaluation(candidate_id: str, eval_id: str):
    """Get offer evaluation"""
    return {"score": 82, "recommendation": "Accept"}

@router.post("/{candidate_id}/counter-strategy/{eval_id}")
async def get_counter_strategy(candidate_id: str, eval_id: str):
    """Get counter-offer strategy"""
    return {"counter_salary": 180000, "tips": []}

@router.get("/{candidate_id}/counter-strategy/{strategy_id}")
async def get_strategy(candidate_id: str, strategy_id: str):
    """Get counter strategy details"""
    return {"strategy_id": strategy_id, "recommendations": []}

@router.get("/{candidate_id}/negotiation-tips")
async def get_tips(candidate_id: str):
    """Get negotiation tips"""
    return {"tips": ["Research market rates", "Practice confidence"]}

@router.post("/{candidate_id}/start-negotiation/{job_id}")
async def start_negotiation(candidate_id: str, job_id: str):
    """Start negotiation session"""
    return {"session_id": "neg-123", "status": "started"}

@router.post("/{candidate_id}/update-negotiation/{session_id}")
async def update_negotiation(candidate_id: str, session_id: str, update: dict):
    """Update negotiation"""
    return {"status": "updated", "session_id": session_id}
