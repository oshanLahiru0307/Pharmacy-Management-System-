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