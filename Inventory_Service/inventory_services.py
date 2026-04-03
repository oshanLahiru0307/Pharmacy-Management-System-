import requests
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import inventory_collection
from schemas import Inventory, UpdateInventory
from models import inventory_serializer

router = APIRouter()

MEDICINE_SERVICE_URL = "http://localhost:8003" 

#validate supplier name
def validate_medicine(medicine_name: str):
    try:
        response = requests.get(f"{MEDICINE_SERVICE_URL}/medicines/medicineName/{medicine_name}")
        return response.status_code == 200
    except:
        return False


# add item to the inventory
@router.post("/inventories")
async def create_items(inventory: Inventory):
    if not validate_medicine(inventory.medicine_name):
        raise HTTPException(status_code=404, detail="Medicine not found")
    result = await inventory_collection.insert_one(inventory.model_dump())
    new_inventory = await inventory_collection.find_one({"_id": result.inserted_id})
    return inventory_serializer(new_inventory)


# Get All inventory
@router.get("/inventories")
async def get_items():
    items = await inventory_collection.find().to_list(length=None)
    return [inventory_serializer(i) for i in items]


# Get Single item
@router.get("/inventories/{id}")
async def get_item(id: str):
    item = await inventory_collection.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=404, detail= "Item not found")
    return inventory_serializer(item)


# Get single items by name
@router.get("/inventories/itemName/{itemName}")
async def get_itemsByName(itemName: str):
    items = await inventory_collection.find({"medicine_name": itemName}).to_list(length=None)
    if not items:
        raise HTTPException(status_code=404, detail= "Item not found")
    return [inventory_serializer(i) for i in items]


# Update item
@router.put("/inventories/{id}")
async def update_item(id: str, inventory: UpdateInventory):
    update_data = {k: v for k, v in inventory.model_dump().items() if v is not None}

    if len(update_data) >= 1:
        result = await inventory_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if result.matched_count and result.matched_count > 0:
            updated_item = await inventory_collection.find_one({"_id": ObjectId(id)})
            if updated_item:
                return inventory_serializer(updated_item)

    raise HTTPException(status_code=404, detail="Item not found")


# Delete item
@router.delete("/inventories/{id}")
async def delete_item(id: str):
    result = await inventory_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}

    raise HTTPException(status_code=404, detail="Item not found")
