# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
from typing import Any
import logging
from models import Customer, UpdateCustomer, Supplier, UpdateSupplier, Medicine, UpdateMedicine, Inventory, UpdateInventory, CreatePrescription, UpdatePrescription, CreateOrder, UpdateOrder, CreatePayment, UpdatePayment
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

logger = logging.getLogger("gateway")

# Service URLs
SERVICES = {
    "customer": "http://localhost:8001",
    "supplier": "http://localhost:8002",
    "medicine": "http://localhost:8003",
    "inventory": "http://localhost:8004",
    "prescription": "http://localhost:8005",
    "order": "http://localhost:8006",
    "payment": "http://localhost:8007"
}

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
    timestamp: str

security = HTTPBearer(auto_error=False)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


PUBLIC_PATHS = {
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
}

def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Security(security),
):
    if request.url.path in PUBLIC_PATHS:
        return None

    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing token")

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload
        return payload  # 👈 user info
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
                            

# Apply authentication to every endpoint by default (except PUBLIC_PATHS)
app = FastAPI(
    title="API Gateway",
    version="1.0.0",
    dependencies=[Depends(verify_token)],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice with enhanced error handling"""
    if service not in SERVICES:
        logger.error(f"Service '{service}' not found in registry")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Service Not Found",
                "message": f"The requested service '{service}' is not available",
                "available_services": list(SERVICES.keys())
            }
        )

    url = f"{SERVICES[service]}{path}"
    logger.info(f"Forwarding {method} request to {service} service: {url}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail={
                        "error": "Method Not Allowed",
                        "message": f"HTTP method '{method}' is not supported",
                        "allowed_methods": ["GET", "POST", "PUT", "DELETE"]
                    }
                )
            
            # Handle different response status codes
            if response.status_code >= 400:
                error_detail = None
                try:
                    error_detail = response.json()
                except:
                    error_detail = {"detail": response.text or "Unknown error"}
                
                logger.warning(f"Service {service} returned error: {response.status_code} - {error_detail}")
                
                raise HTTPException(
                    status_code=response.status_code,
                    detail={
                        "error": f"Service Error ({response.status_code})",
                        "message": error_detail.get("detail", "An error occurred in the microservice"),
                        "service": service,
                        "path": path
                    }
                )
            
            # Return successful response
            response_data = None
            if response.text:
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw": response.text}
            
            return JSONResponse(
                content=response_data,
                status_code=response.status_code
            )
            
        except httpx.TimeoutException as e:
            logger.error(f"Timeout connecting to {service} service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail={
                    "error": "Gateway Timeout",
                    "message": f"The {service} service did not respond in time",
                    "service": service,
                    "timeout": "30 seconds"
                }
            )
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {service} service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "Service Unavailable",
                    "message": f"Unable to connect to {service} service. Please check if the service is running.",
                    "service": service,
                    "url": url
                }
            )
        except httpx.RequestError as e:
            logger.error(f"Request error to {service} service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "error": "Bad Gateway",
                    "message": f"Error communicating with {service} service",
                    "service": service,
                    "error_details": str(e)
                }
            )
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error forwarding request to {service}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while processing your request",
                    "service": service
                }
            )


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "available_services": list(SERVICES.keys()),
        "version": "1.0.0"
    }

# Customer Service Routes — forwards to Customer_Service (localhost:8001) /customers
@app.get("/gateway/customers")
async def get_all_customers():
    """Get all customers through gateway"""
    return await forward_request("customer", "/customers", "GET")


@app.get("/gateway/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get a customer by ID through gateway"""
    return await forward_request("customer", f"/customers/{customer_id}", "GET")


@app.post("/gateway/customers")
async def create_customer(customer: Customer):
    """Create a new customer through gateway"""
    return await forward_request("customer", "/customers", "POST", json=customer.model_dump())


@app.put("/gateway/customers/{customer_id}")
async def update_customer(customer_id: str, customer: UpdateCustomer):
    """Update a customer through gateway"""
    body = customer.model_dump(exclude_none=True)
    return await forward_request("customer", f"/customers/{customer_id}", "PUT", json=body)


@app.delete("/gateway/customers/{customer_id}")
async def delete_customer(customer_id: str):
    """Delete a customer through gateway"""
    return await forward_request("customer", f"/customers/{customer_id}", "DELETE")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  
    )