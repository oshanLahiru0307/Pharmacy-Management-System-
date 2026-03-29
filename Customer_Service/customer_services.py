from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import customer_collection
from schemas import Customer, UpdateCustomer
from models import customer_serializer

router = APIRouter()

# Create Customer
@router.post("/customers")
async def create_customer(customer: Customer):
    result = await customer_collection.insert_one(customer.model_dump())
    new_customer = await customer_collection.find_one({"_id": result.inserted_id})
    return customer_serializer(new_customer)


# Get All Customers
@router.get("/customers")
async def get_customers():
    customers = await customer_collection.find().to_list(length=None)
    return [customer_serializer(c) for c in customers]


# Get Single Customer
@router.get("/customers/{id}")
async def get_customer(id: str):
    customer = await customer_collection.find_one({"_id": ObjectId(id)})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_serializer(customer)


# Update Customer
@router.put("/customers/{id}")
async def update_customer(id: str, customer: UpdateCustomer):
    update_data = {k: v for k, v in customer.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await customer_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_customer = await customer_collection.find_one({"_id": ObjectId(id)})
            return customer_serializer(updated_customer)

    raise HTTPException(status_code=404, detail="Customer not found or no changes made")


# Delete Customer
@router.delete("/customers/{id}")
async def delete_customer(id: str):
    result = await customer_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "Customer deleted successfully"}

    raise HTTPException(status_code=404, detail="Customer not found")
