from fastapi import HTTPException, Depends, Request, Response
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.api_key_service import APIKeyService
from app.services.usage_service import UsageService
from app.core.rate_limiter import rate_limiter


async def verify_api_key(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
) -> str:

    api_key = request.headers.get("X-API-Key")

    # ---------------- Missing API Key ----------------
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )

    api_key_service = APIKeyService(db)
    usage_service = UsageService(db)

    # ---------------- Validate Key ----------------
    is_valid = api_key_service.validate_api_key(api_key)

    if not is_valid:
        usage_service.log_request(
            api_key="INVALID",
            endpoint=str(request.url.path),
            method=request.method,
            status_code=401,
            ip_address=request.client.host
        )
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # ---------------- Rate Limit Check ----------------
    is_allowed, remaining = rate_limiter.check_rate_limit(api_key)

    if not is_allowed:
        usage_service.log_request(
            api_key=api_key,
            endpoint=str(request.url.path),
            method=request.method,
            status_code=429,
            ip_address=request.client.host
        )

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
            headers={"Retry-After": "60"}
        )

    # ---------------- SUCCESS FLOW ----------------
    api_key_service.update_last_used(api_key)

    usage_service.log_request(
        api_key=api_key,
        endpoint=str(request.url.path),
        method=request.method,
        status_code=200,
        ip_address=request.client.host
    )

    # ---------------- Rate Limit Headers ----------------
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    request.state.api_key = api_key
    request.state.rate_limit_remaining = remaining

    return api_key


def get_rate_limit_remaining(request: Request):
    return getattr(request.state, "rate_limit_remaining", None)