from fastapi import APIRouter, Depends, Request
from app.core.dependencies import verify_api_key, get_rate_limit_remaining
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["Protected APIs"])

class DataResponse(BaseModel):
    message: str
    data: dict
    rate_limit_remaining: Optional[int]

@router.get("/protected-data")
async def get_protected_data(
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    remaining = get_rate_limit_remaining(request)
    
    return DataResponse(
        message="Access granted! This is protected data.",
        data={
            "info": "This data is only available with valid API key",
            "timestamp": "2024-01-01T00:00:00Z",
            "user_data": "Confidential information"
        },
        rate_limit_remaining=remaining
    )

@router.get("/user-info")
async def get_user_info(
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    remaining = get_rate_limit_remaining(request)
    
    return DataResponse(
        message="User information retrieved successfully",
        data={
            "user_id": "12345",
            "name": "John Doe",
            "email": "john@example.com",
            "plan": "Premium"
        },
        rate_limit_remaining=remaining
    )

@router.post("/process-data")
async def process_data(
    request: Request,
    data: dict,
    api_key: str = Depends(verify_api_key)
):
    remaining = get_rate_limit_remaining(request)
    
    return DataResponse(
        message="Data processed successfully",
        data={
            "received": data,
            "processed": True,
            "result": "Success"
        },
        rate_limit_remaining=remaining
    )