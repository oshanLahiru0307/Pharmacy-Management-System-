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