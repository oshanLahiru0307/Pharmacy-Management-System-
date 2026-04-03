from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# Nested Order Item
class OrderItem(BaseModel):
    medicine_name: str
    quantity: int = Field(..., ge=1)
    price: float = Field(..., gt=0)


# Create Order
class CreateOrder(BaseModel):
    order_id: str
    customer_id: str
    items: List[OrderItem]
    prescription_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Update Order
class UpdateOrder(BaseModel):
    customer_id: str | None = None
    items: List[OrderItem] | None = None
    prescription_id: str | None = None   # optional link
    status: Literal["PENDING", "COMPLETED", "CANCELLED"] | None = None
    created_at: datetime
    updated_at: datetime


# Response Schema
class OrderResponse(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    prescription_id: Optional[str] = None
    created_at: datetime