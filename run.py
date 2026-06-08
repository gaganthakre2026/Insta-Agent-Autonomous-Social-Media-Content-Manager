#!/usr/bin/env python
"""Startup script for Insta-Agent backend."""
import os
import sys
from pathlib import Path


# Add the backend directory to Python path.
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("BACKEND_PORT", 8000))

    print("Starting Insta-Agent Backend...")
    print(f"Working directory: {backend_dir}")
    print(f"Python path: {sys.path[0]}")
    print(f"Port: {port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
