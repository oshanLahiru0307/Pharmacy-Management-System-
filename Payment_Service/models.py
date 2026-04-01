def payment_serializer(payment) -> dict:
    return {
        "id": str(payment["_id"]),
        "order_id": payment["order_id"],
        "amount": payment["amount"],
        "method": payment["method"],
        "transaction_id": payment.get("transaction_id"),
        "status": payment["status"],
        "notes": payment.get("notes"),
        "created_at": payment["created_at"],
        "updated_at": payment["updated_at"]
    }