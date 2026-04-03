def order_serializer(order) -> dict:
    return {
        "id": str(order["_id"]),
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "items": [
            {
                "medicine_name": item["medicine_name"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            for item in order["items"]
        ],
        "total_amount": order.get("total_amount", 0),
        "status": order.get("status", "PENDING"),
        "prescription_id": order.get("prescription_id"),
        "created_at": order["created_at"],
        "updated_at": order["updated_at"],

    }