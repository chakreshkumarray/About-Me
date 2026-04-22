"""Pydantic models for type safety"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class PatientInfo(BaseModel):
    """Patient information schema"""
    patient_id: str
    name: str
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    medical_history: Optional[str] = None


class HCPInfo(BaseModel):
    """Healthcare Provider information schema"""
    provider_id: str
    name: str
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Message(BaseModel):
    """Chat message schema"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request schema"""
    user_id: str
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response schema"""
    conversation_id: str
    response: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime


class FormData(BaseModel):
    """Form data schema for structured information"""
    user_id: str
    form_type: str  # "patient_info", "hcp_info", etc.
    data: Dict[str, Any]
    submission_date: Optional[datetime] = None

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_session"

class FormExtraction(BaseModel):
    hcpName: Optional[str] = ""
    topics: Optional[str] = ""
    sentiment: Optional[str] = ""
    samples: List[str] = []