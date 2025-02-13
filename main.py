from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import asyncio

app = FastAPI(title="LinkedIn Job Hunter API")

@app.post("/api/v1/bulk-apply")
async def bulk_apply(
    params: JobParameters,
    max_applications: int = 20,
    db: Session = Depends(get_db)
):
    """Apply to multiple jobs matching the specified parameters"""
    try:
        bulk_service = BulkApplicationService(
            db=db,
            linkedin_scraper=LinkedInScraper(),
            resume_tailor=ResumeTailor(),
            job_applier=LinkedInJobApplier()
        )
        
        # Start bulk application process
        await bulk_service.process_bulk_applications(
            params.dict(),
            max_applications
        )
        
        return {"message": "Bulk application process started"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start bulk application process: {str(e)}"
        )

@app.get("/api/v1/application-status")
async def get_application_status(
    db: Session = Depends(get_db)
):
    """Get status of all job applications"""
    applications = db.query(JobApplication).all()
    return {
        "total": len(applications),
        "applied": len([a for a in applications if a.status == "applied"]),
        "failed": len([a for a in applications if a.status == "failed"]),
        "pending": len([a for a in applications if a.status == "pending"]),
        "applications": applications
    }