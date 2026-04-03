import requests
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import medicine_collection
from schemas import Medicine, UpdateMedicine
from models import medicine_serializer

router = APIRouter()

SUPPLIER_SERVICE_URL = "http://localhost:8002"  # Supplier service

#validate supplier name
def validate_supplier(supplier_name: str):
    try:
        response = requests.get(f"{SUPPLIER_SERVICE_URL}/suppliers/supplier/{supplier_name}")
        return response.status_code == 200
    except:
        return False


# Create medicine
@router.post("/medicines")
async def create_medicine(medicine: Medicine):
    #validate supplier details before save medicine
    if not validate_supplier(medicine.supplier):
        raise HTTPException(status_code=400, detail="Invalid supplier")
    result = await medicine_collection.insert_one(medicine.model_dump())
    new_medicine = await medicine_collection.find_one({"_id": result.inserted_id})
    return medicine_serializer(new_medicine)


# Get All medicine
@router.get("/medicines")
async def get_medicines():
    medicines = await medicine_collection.find().to_list(length=None)
    return [medicine_serializer(c) for c in medicines]


# Get Single medicine
@router.get("/medicines/{id}")
async def get_medicine(id: str):
    medicine = await medicine_collection.find_one({"_id": ObjectId(id)})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine_serializer(medicine)


# Get Single medicine by name
@router.get("/medicines/medicineId/{medicineId}")
async def get_medicine(medicineId: str):
    medicine = await medicine_collection.find_one({"medicine_id": medicineId})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine_serializer(medicine)


# Get Single medicine by name
@router.get("/medicines/medicineName/{medicineName}")
async def get_medicine(medicineName: str):
    medicine = await medicine_collection.find_one({"name": medicineName})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine_serializer(medicine)
    

# Update medicine
@router.put("/medicines/{id}")
async def update_medicine(id: str, medicine: UpdateMedicine):
    update_data = {k: v for k, v in medicine.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await medicine_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_medicine = await medicine_collection.find_one({"_id": ObjectId(id)})
            return medicine_serializer(updated_medicine)

    raise HTTPException(status_code=404, detail="Medicine not found or no changes made")


# Delete Customer
@router.delete("/medicines/{id}")
async def delete_medicine(id: str):
    result = await medicine_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "Medicine deleted successfully"}

    raise HTTPException(status_code=404, detail="Medicine not found")
