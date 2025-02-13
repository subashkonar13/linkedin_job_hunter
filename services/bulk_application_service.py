from typing import List, Dict
import asyncio
from datetime import datetime
import logging
from sqlalchemy.orm import Session

class BulkApplicationService:
    def __init__(self, db: Session, linkedin_scraper, resume_tailor, job_applier):
        self.db = db
        self.scraper = linkedin_scraper
        self.resume_tailor = resume_tailor
        self.job_applier = job_applier
        self.logger = logging.getLogger(__name__)
        
    async def process_bulk_applications(
        self, 
        job_params: Dict,
        max_applications: int = 20
    ):
        """Process multiple job applications in parallel"""
        jobs = await self.scraper.search_jobs(job_params)
        
        # Filter jobs based on criteria
        filtered_jobs = self._filter_jobs(jobs, job_params)
        
        # Limit number of applications
        jobs_to_apply = filtered_jobs[:max_applications]
        
        # Process applications in batches
        batch_size = 5
        for i in range(0, len(jobs_to_apply), batch_size):
            batch = jobs_to_apply[i:i + batch_size]
            tasks = [
                self._process_single_application(job)
                for job in batch
            ]
            await asyncio.gather(*tasks)
            
    async def _process_single_application(self, job: Dict):
        """Process a single job application"""
        try:
            # Create database entry
            application = self._create_application_entry(job)
            
            # Tailor resume
            tailored_resume = await self.resume_tailor.tailor_resume(
                job['description'],
                self.base_resume_id
            )
            
            # Apply to job
            success = await self.job_applier.apply_to_job(
                job['url'],
                tailored_resume
            )
            
            # Update database
            self._update_application_status(
                application.id,
                'applied' if success else 'failed'
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process application: {str(e)}")
            self._update_application_status(
                application.id,
                'failed',
                str(e)
            )
            
    def _filter_jobs(self, jobs: List[Dict], params: Dict) -> List[Dict]:
        """Filter jobs based on parameters"""
        filtered = []
        for job in jobs:
            if self._matches_criteria(job, params):
                filtered.append(job)
        return filtered
        
    def _matches_criteria(self, job: Dict, params: Dict) -> bool:
        """Check if job matches specified criteria"""
        if params.get('min_salary'):
            if not self._meets_salary_requirement(
                job.get('salary', ''), 
                params['min_salary']
            ):
                return False
                
        if params.get('visa_sponsorship'):
            if not self._has_visa_sponsorship(job['description']):
                return False
                
        return True
