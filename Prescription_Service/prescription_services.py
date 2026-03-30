from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import prescription_collection
from schemas import CreatePrescription, UpdatePrescription
from models import prescription_serializer

router = APIRouter()

# Create prescription
@router.post("/prescriptions")
async def create_prescription(prescription: CreatePrescription):
    result = await prescription_collection.insert_one(prescription.model_dump())
    new_prescription = await prescription_collection.find_one({"_id": result.inserted_id})
    return prescription_serializer(new_prescription)


# Get All prescriptions
@router.get("/prescriptions")
async def get_prescriptions():
    prescriptions = await prescription_collection.find().to_list(length=None)
    return [prescription_serializer(p) for p in prescriptions]


# Get Single prescription
@router.get("/prescriptions/{id}")
async def get_prescription(id: str):
    prescription = await prescription_collection.find_one({"_id": ObjectId(id)})
    if not prescription:
        raise HTTPException(status_code=404, detail="prescription not found")
    return prescription_serializer(prescription)


# Update prescription
@router.put("/prescriptions/{id}")
async def update_prescription(id: str, prescription: UpdatePrescription):
    update_data = {k: v for k, v in prescription.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await prescription_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if result.matched_count and result.matched_count > 0:
            updated_prescription = await prescription_collection.find_one({"_id": ObjectId(id)})
            if updated_prescription:
                return prescription_serializer(updated_prescription)

    raise HTTPException(status_code=404, detail="prescription not found or no changes made")


# Delete Customer
@router.delete("/prescriptions/{id}")
async def delete_prescription(id: str):
    result = await prescription_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "prescription deleted successfully"}

    raise HTTPException(status_code=404, detail="prescription not found")
