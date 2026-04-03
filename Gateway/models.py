from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional, List
from datetime import datetime

class Customer(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class UpdateCustomer(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

from pydantic import BaseModel, EmailStr

class Supplier(BaseModel):
    supplier_name: str
    email: EmailStr
    phone: str
    address: str

class UpdateSupplier(BaseModel):
    supplier_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

from pydantic import BaseModel

class Medicine(BaseModel):
    medicine_id: str
    name: str
    category: str
    price: float
    supplier: str
    manufacturer: str

class UpdateMedicine(BaseModel):
    medicine_id: str | None = None
    name: str | None = None
    category: str | None = None
    price: float | None = None
    supplier: str | None = None
    manufacturer: str | None = None

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

class PrescriptionItem(BaseModel):
    medicine_id: str
    dosage: str                 
    frequency: str              
    duration: str               


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
