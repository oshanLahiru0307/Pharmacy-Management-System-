from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import order_collection
from schemas import CreateOrder, UpdateOrder
from models import order_serializer

router = APIRouter()



# Create order
@router.post("/orders")
async def create_order(order: CreateOrder):

    order_dict = order.model_dump()  # convert Pydantic model to dict

    # Calculate total_amount
    order_dict["total_amount"] = sum(item["quantity"] * item["price"] for item in order_dict["items"])

    # Ensure fields expected by serializer exist
    order_dict.setdefault("status", "PENDING")
    order_dict.setdefault("prescription_id", None)

    result = await order_collection.insert_one(order_dict)
    new_order= await order_collection.find_one({"_id": result.inserted_id})
    return order_serializer(new_order)


# Get All orders
@router.get("/orders")
async def get_orders():
    orders = await order_collection.find().to_list(length=None)
    return [order_serializer(o) for o in orders]


# Get Single Customer
@router.get("/orders/{id}")
async def get_orders(id: str):
    order = await order_collection.find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_serializer(order)


# Update Customer
@router.put("/orders/{id}")
async def update_order(id: str, order: UpdateOrder):
    # Fetch first so we can (a) verify existence and (b) compute total_amount safely.
    existing_order = await order_collection.find_one({"_id": ObjectId(id)})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = {k: v for k, v in order.model_dump().items() if v is not None}
    if not update_data:
        # Nothing to update; return current order (same behavior style as create/serializer safety).
        return order_serializer(existing_order)

    # If items are being updated, recompute total_amount (same rule as create_order).
    if "items" in update_data:
        update_data["total_amount"] = sum(
            item["quantity"] * item["price"] for item in update_data["items"]
        )

    result = await order_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data},
    )

    # Even if Mongo reports 0 modified (same data), return the stored order.
    updated_order = await order_collection.find_one({"_id": ObjectId(id)})
    if not updated_order:
        # Should be rare (document deleted between calls).
        raise HTTPException(status_code=404, detail="Order not found")

    # Keep serializer robust for older documents missing total_amount/status.
    updated_order.setdefault("status", "PENDING")
    updated_order.setdefault("prescription_id", None)
    if "total_amount" not in updated_order and "items" in updated_order:
        updated_order["total_amount"] = sum(
            item["quantity"] * item["price"] for item in updated_order["items"]
        )

    return order_serializer(updated_order)


# Delete Customer
@router.delete("/orders/{id}")
async def delete_order(id: str):
    result = await order_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"message": "Order deleted successfully"}

    raise HTTPException(status_code=404, detail="Order not found")
