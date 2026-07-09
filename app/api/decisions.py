from fastapi import APIRouter

router = APIRouter(prefix="/api/decisions", tags=["Decisions"])

@router.post("/{candidate_id}/{job_id}")
async def generate_decision(candidate_id: str, job_id: str):
    """Generate hiring decision"""
    return {"decision": "STRONG YES", "score": 88}

@router.post("/feedback/{candidate_id}/{job_id}")
async def generate_feedback(candidate_id: str, job_id: str):
    """Generate feedback"""
    return {"feedback": "Great match!", "strengths": []}

@router.post("/offers/{candidate_id}")
async def generate_offer(candidate_id: str, offer_data: dict):
    """Generate offer letter"""
    return {"status": "success", "offer_letter": "..."}

@router.get("/")
async def list_decisions():
    """List all decisions"""
    return {"decisions": [], "total": 0}

@router.post("/{decision_id}/send")
async def send_decision(decision_id: str):
    """Send decision letter"""
    return {"status": "sent"}
