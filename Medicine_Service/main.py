from fastapi import FastAPI
from medicine_services import router

app = FastAPI(title="Medicine Microservice")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8003,
        reload=True  
    )