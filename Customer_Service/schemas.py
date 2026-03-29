from pydantic import BaseModel, EmailStr

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