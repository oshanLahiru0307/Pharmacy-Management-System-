from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class Inventory(BaseModel):
    medicine_name: str                      
    quantity: int = Field(..., gt=0)      
    type: Literal["IN", "OUT"]            
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None

class UpdateInventory(BaseModel):
    medicine_name: str | None = None                     
    quantity: int = Field(..., gt=0)     
    type: Literal["IN", "OUT"] | None = None          
    batch_number: str | None = None
    expiry_date: datetime | None = None