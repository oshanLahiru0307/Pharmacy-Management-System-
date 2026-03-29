def customer_serializer(customer) -> dict:
    return {
        "id": str(customer["_id"]),
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "address": customer["address"]
    }