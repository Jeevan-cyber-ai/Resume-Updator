from fastapi import APIRouter, HTTPException
from models.improver import ImproveRequest, ImproveResponse
from services.improver_graph import run_improver_graph

router = APIRouter()

@router.post("/improve", response_model=ImproveResponse)
async def improve_section(req: ImproveRequest):
    if not req.section.strip():
        raise HTTPException(status_code=400, detail="section is required.")
        
    state_input = {
        "section": req.section,
        "resume_data": req.resume_data,
        "job_title": req.job_title,
        "user_input": req.user_input,
        "feedback_history": [msg.dict() for msg in req.feedback_history] if req.feedback_history else [],
        "generated_output": ""
    }
    
    try:
        final_state = run_improver_graph(state_input)
        
        return ImproveResponse(
            message=f"Successfully generated improvement for {req.section}",
            generated_output=final_state.get("generated_output", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
