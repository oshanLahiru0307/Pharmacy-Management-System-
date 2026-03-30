def supplier_serializer(supplier) -> dict:
    return {
        "id": str(supplier["_id"]),
        "supplier_name": supplier["supplier_name"],
        "email": supplier["email"],
        "phone": supplier["phone"],
        "address": supplier["address"]
    }