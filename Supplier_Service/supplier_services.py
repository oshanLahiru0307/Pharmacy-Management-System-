from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import supplier_collection
from schemas import Supplier, UpdateSupplier
from models import supplier_serializer

router = APIRouter()

# Create supplier
@router.post("/suppliers")
async def create_supplier(supplier: Supplier):
    result = await supplier_collection.insert_one(supplier.model_dump())
    new_supplier = await supplier_collection.find_one({"_id": result.inserted_id})
    return supplier_serializer(new_supplier)


# Get All suppliers
@router.get("/suppliers")
async def get_suppliers():
    suppliers = await supplier_collection.find().to_list(length=None)
    return [supplier_serializer(c) for c in suppliers]


# Get Single supplier
@router.get("/suppliers/{id}")
async def get_supplier(id: str):
    supplier = await supplier_collection.find_one({"_id": ObjectId(id)})
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier_serializer(supplier)


#Get Single supplier by name
@router.get("/suppliers/supplier/{supplierName}")
async def get_supplier(supplierName: str):
    supplier = await supplier_collection.find_one({"supplier_name": supplierName})
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier_serializer(supplier)



# Update suppliers
@router.put("/suppliers/{id}")
async def update_supplier(id: str, supplier: UpdateSupplier):
    update_data = {k: v for k, v in supplier.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await supplier_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_supplier = await supplier_collection.find_one({"_id": ObjectId(id)})
            return supplier_serializer(updated_supplier)

    raise HTTPException(status_code=404, detail="Supplier not found or no changes made")


# Delete supplier
@router.delete("/suppliers/{id}")
async def delete_supplier(id: str):
    result = await supplier_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "Supplier deleted successfully"}

    raise HTTPException(status_code=404, detail="Supplier not found")
