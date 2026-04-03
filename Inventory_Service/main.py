from fastapi import FastAPI
from inventory_services import router

app = FastAPI(title="Inventory Microservice")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8004,
        reload=True  
    )