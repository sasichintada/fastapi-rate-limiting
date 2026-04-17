from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.api import auth, protected
from app.core.config import settings
from app.database.database import engine, Base
import time

# ---------------- DB INIT ----------------
Base.metadata.create_all(bind=engine)

# ---------------- APP INIT ----------------
app = FastAPI(
    title="FastAPI Rate Limiting Service",
    description="API Key Management + Rate Limiting System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST LOG MIDDLEWARE ----------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


# ---------------- GLOBAL EXCEPTION HANDLER ----------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        }
    )


# ---------------- SWAGGER API KEY AUTHORIZE BUTTON ----------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"ApiKeyAuth": []}
            ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ---------------- ROUTES ----------------
app.include_router(auth.router)
app.include_router(protected.router)


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "rate_limit": f"{settings.RATE_LIMIT_PER_MINUTE} requests/minute"
    }


# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


# ---------------- RUN ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )