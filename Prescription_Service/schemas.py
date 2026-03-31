from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class PrescriptionItem(BaseModel):
    medicine_name: str
    dosage: str                 # e.g., "500mg"
    frequency: str              # e.g., "Twice a day"
    duration: str               # e.g., "5 days"


class CreatePrescription(BaseModel):
    customer_id: str            
    doctor_name: str
    items: List[PrescriptionItem]
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    

class UpdatePrescription(BaseModel):
    customer_id: str | None = None          
    doctor_name: str | None = None
    items: Optional[List[PrescriptionItem]] = None
    notes: Optional[str] = None
    updated_at: datetime
