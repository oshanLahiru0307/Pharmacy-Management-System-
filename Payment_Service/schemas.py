from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


# Create Payment
class CreatePayment(BaseModel):
    order_id: str                       
    amount: float = Field(..., gt=0)    
    method: Literal["CASH", "CARD", "ONLINE"]
    status: Optional[Literal["PENDING", "SUCCESS", "FAILED", "REFUNDED"]] = None  
    transaction_id: Optional[str] = None       
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Update Payment
class UpdatePayment(BaseModel):
    order_id: str | None = None                      
    amount: float = Field(..., gt=0)
    method: Literal["CASH", "CARD", "ONLINE"] | None = None
    status: Optional[Literal["PENDING", "SUCCESS", "FAILED", "REFUNDED"]] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
