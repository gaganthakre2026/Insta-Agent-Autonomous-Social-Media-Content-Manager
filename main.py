from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa: F401 - Import registers SQLAlchemy models with Base metadata.
from apis.v1 import analytics as analytics_api
from apis.v1 import auth as auth_api
from apis.v1 import content as content_api
from apis.v1 import posts as posts_api
from db import Base, engine

app = FastAPI(title="Instagram Agent API", version="0.2.0")


@app.on_event("startup")
def init_database() -> None:
    """Create tables automatically for local development."""
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.2.0"}


@app.get("/")
def home():
    return {"message": "Instagram Agent Backend Running"}


@app.get("/api/v1/services/status")
def check_services_status():
    import requests

    services_status = {
        "backend": {
            "status": "RUNNING",
            "url": "http://localhost:8000",
            "port": 8000,
        },
        "stable_diffusion": {
            "status": "NOT RUNNING",
            "url": "http://localhost:7860",
            "port": 7860,
            "fix_instructions": "Start with: webui-user.bat in AUTOMATIC1111 folder",
        },
        "summary": "",
    }

    try:
        sd_response = requests.get("http://localhost:7860/api/sd-models", timeout=5)
        if sd_response.status_code == 200:
            services_status["stable_diffusion"]["status"] = "RUNNING"
            services_status["summary"] = "All services running. Ready to generate images."
        else:
            services_status["summary"] = "Stable Diffusion is reachable but not responding correctly."
    except requests.exceptions.RequestException:
        services_status["summary"] = "Stable Diffusion is not running. Start webui-user.bat first."

    all_running = (
        services_status["backend"]["status"] == "RUNNING"
        and services_status["stable_diffusion"]["status"] == "RUNNING"
    )

    return {
        "services": services_status,
        "all_running": all_running,
    }


@app.get("/api/v1/content/test-connection")
def test_connection():
    return {
        "status": "Backend is running perfectly.",
        "version": "0.2.0",
        "message": "Your frontend can connect to the backend",
        "connection_test": "SUCCESS",
        "endpoints": {
            "health": "/health",
            "status": "/api/v1/services/status",
            "test": "/api/v1/content/test-connection",
            "generate": "/api/v1/content/generate-content",
            "docs": "/docs",
        },
    }


@app.get("/api/v1/debug/connection-info")
def debug_connection_info():
    import socket

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return {
        "server_info": {
            "hostname": hostname,
            "local_ip": local_ip,
            "listening_on": "http://127.0.0.1:8000",
            "accessible_from": "http://localhost:8000",
        },
        "cors_status": "ENABLED",
        "frontend_should_use": "http://127.0.0.1:8000",
        "test_these_endpoints": {
            "/health": "Simple health check",
            "/api/v1/content/test-connection": "Test frontend connection",
            "/api/v1/services/status": "Check all services",
            "/docs": "Interactive API documentation",
        },
    }


def mount_router(prefix: str, router) -> None:
    app.include_router(router, prefix=prefix)


for prefix in ("/api/v1/content", "/content"):
    mount_router(prefix, content_api.router)

for prefix in ("/api/v1/auth", "/auth"):
    mount_router(prefix, auth_api.router)

for prefix in ("/api/v1/analytics", "/analytics"):
    mount_router(prefix, analytics_api.router)

for prefix in ("/api/v1/posts", "/posts"):
    mount_router(prefix, posts_api.router)
