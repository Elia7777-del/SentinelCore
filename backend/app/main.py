from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.session import Base, engine
from app.api.health import router as health_router
from app.api.events import router as events_router
from app.api.auth import router as auth_router
from app.api.incidents import router as incidents_router
from app.api.agents import router as agents_router
from app.api.dashboard import router as dashboard_router
from app.api.enterprise import router as enterprise_router
from app.api.health import router as health_router
from app.api.webauthn import router as webauthn_router
from app.api.ai_analysis import router as ai_analysis_router
from app.api.org_settings import router as org_settings_router
from app.models import Organization, Agent, SecurityEvent, User, AuditLog, Incident, RefreshSession  # noqa

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="7.0",
    description="SentinelCore secure remote cybersecurity platform foundation.",
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Sentinel-Agent-Token"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    if settings.require_https and request.url.path not in ("/health", "/docs", "/openapi.json"):
        forwarded = request.headers.get("x-forwarded-proto")
        if request.url.scheme != "https" and forwarded != "https":
            return JSONResponse(status_code=400, content={"detail": "HTTPS is required"})
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api/") else "private"
    if request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(incidents_router)
app.include_router(agents_router)
app.include_router(dashboard_router)
app.include_router(enterprise_router)
app.include_router(health_router)
app.include_router(webauthn_router)
app.include_router(ai_analysis_router)
app.include_router(org_settings_router)

@app.get("/")
def root():
    return {
        "name": "SentinelCore",
        "service": "central-security-platform",
        "status": "online",
        "api_version": "v1",
    }
