def medicine_serializer(medicine) -> dict:
    return {
        "id": str(medicine["_id"]),
        "medicine_id": medicine["medicine_id"],
        "name": medicine["name"],
        "category": medicine["category"],
        "price": medicine["price"],
        "supplier": medicine["supplier"],
        "manufacturer": medicine["manufacturer"]
    }