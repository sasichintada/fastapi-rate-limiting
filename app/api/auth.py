from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database.database import get_db
from app.services.api_key_service import APIKeyService
from app.services.usage_service import UsageService
from app.core.dependencies import verify_api_key
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

class APIKeyRequest(BaseModel):
    client_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')

class APIKeyResponse(BaseModel):
    api_key: str
    client_name: str
    email: str
    message: str

@router.post("/generate-key", response_model=APIKeyResponse)
async def generate_api_key(
    request: APIKeyRequest,
    db: Session = Depends(get_db)
):
    service = APIKeyService(db)
    api_key = service.create_api_key(request.client_name, request.email)
    
    return APIKeyResponse(
        api_key=api_key.api_key,
        client_name=api_key.client_name,
        email=api_key.email,
        message="API key generated successfully. Please save it securely."
    )

@router.get("/usage-stats")
async def get_usage_stats(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
    hours: int = 24
):
    usage_service = UsageService(db)
    stats = usage_service.get_usage_stats(api_key, hours)
    return stats

@router.post("/revoke-key/{api_key_to_revoke}")
async def revoke_api_key(
    api_key_to_revoke: str,
    admin_key: str,
    db: Session = Depends(get_db)
):
    if admin_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin credentials")
    
    service = APIKeyService(db)
    success = service.revoke_api_key(api_key_to_revoke)
    
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"message": "API key revoked successfully"}

@router.get("/list-keys")
async def list_api_keys(
    admin_key: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    if admin_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin credentials")
    
    service = APIKeyService(db)
    keys = service.get_all_keys(skip, limit)
    
    return {"api_keys": [
        {
            "api_key": key.api_key,
            "client_name": key.client_name,
            "email": key.email,
            "created_at": key.created_at.isoformat() if key.created_at else None,
            "total_requests": key.total_requests,
            "is_active": key.is_active
        } for key in keys
    ]}