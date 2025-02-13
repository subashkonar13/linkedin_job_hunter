from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    salary = Column(String)
    url = Column(String)
    description = Column(String)
    status = Column(String)  # pending, applied, failed
    applied_at = Column(DateTime, default=datetime.utcnow)
    resume_version = Column(String)
    application_response = Column(JSON)
    error_message = Column(String)

class RateLimit(Base):
    __tablename__ = 'rate_limits'
    
    id = Column(Integer, primary_key=True)
    endpoint = Column(String)
    last_access = Column(DateTime)
    count = Column(Integer)
