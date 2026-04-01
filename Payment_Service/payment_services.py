from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import payment_collection
from schemas import CreatePayment, UpdatePayment
from models import payment_serializer

router = APIRouter()

# Create payment
@router.post("/payments")
async def create_payment(payment: CreatePayment):
    result = await payment_collection.insert_one(payment.model_dump())
    new_payment = await payment_collection.find_one({"_id": result.inserted_id})
    return payment_serializer(new_payment)


# Get All payments
@router.get("/payments")
async def get_payments():
    payments = await payment_collection.find().to_list(length=None)
    return [payment_serializer(p) for p in payments]


# Get Single payment
@router.get("/payments/{id}")
async def get_payment(id: str):
    payment = await payment_collection.find_one({"_id": ObjectId(id)})
    if not payment:
        raise HTTPException(status_code=404, detail="payment not found")
    return payment_serializer(payment)


# Update payment
@router.put("/payments/{id}")
async def update_payment(id: str, payment: UpdatePayment):
    update_data = {k: v for k, v in payment.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await payment_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_payment = await payment_collection.find_one({"_id": ObjectId(id)})
            return payment_serializer(updated_payment)

    raise HTTPException(status_code=404, detail="payment not found or no changes made")


# Delete payment
@router.delete("/payments/{id}")
async def delete_payment(id: str):
    result = await payment_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "payment deleted successfully"}

    raise HTTPException(status_code=404, detail="payment not found")
