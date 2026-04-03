def inventory_serializer(inventory) -> dict:
    return {
        "id": str(inventory["_id"]),
        "medicine_name": inventory["medicine_name"],
        "quantity": inventory["quantity"],
        "type": inventory["type"],
        "batch_number": inventory["batch_number"],
        "expiry_date": inventory["expiry_date"]
    }