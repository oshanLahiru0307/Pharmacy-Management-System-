def prescription_serializer(prescription) -> dict:
    return {
        "id": str(prescription["_id"]),
        "customer_id": prescription["customer_id"],
        "doctor_name": prescription["doctor_name"],
        "items": [
            {
                "medicine_name": item["medicine_name"],
                "dosage": item["dosage"],
                "frequency": item["frequency"],
                "duration": item["duration"]
            }
            for item in prescription["items"]
        ],
        "notes": prescription["notes"],
        "created_at": prescription["created_at"],
        "updated_at": prescription["updated_at"]

    }