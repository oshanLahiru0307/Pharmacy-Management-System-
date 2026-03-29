from fastapi import FastAPI
from customer_services import router

app = FastAPI(title="Customer Microservice")

app.include_router(router)