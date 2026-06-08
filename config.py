"""Configuration settings for the Insta-Agent backend."""
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


PLACEHOLDER_ENV_VALUES = {
    "",
    "changeme",
    "change_me",
    "your_app_id",
    "your_app_secret",
    "your_client_id",
    "your_client_secret",
    "your_instagram_app_id_here",
    "your_instagram_app_secret_here",
    "your-instagram-app-id",
    "your-instagram-app-secret",
}


def _load_workspace_root_env() -> None:
    backend_env_path = Path(__file__).resolve().parent / ".env"
    root_env_path = backend_env_path.parent.parent / ".env"
    if not root_env_path.exists():
        return

    backend_env_values: dict[str, str] = {}
    if backend_env_path.exists() and backend_env_path.stat().st_size > 0:
        with backend_env_path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                backend_env_values[key.strip()] = value.strip().strip('"').strip("'")

    with root_env_path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            backend_value = backend_env_values.get(key)
            backend_has_real_value = bool(
                backend_value
                and backend_value.strip()
                and backend_value.strip().lower() not in PLACEHOLDER_ENV_VALUES
            )

            if key and key not in os.environ and not backend_has_real_value:
                os.environ[key] = value


class Settings(BaseSettings):
    """Application settings."""

    # Database - Using SQLite for development (no server needed)
    DATABASE_URL: str = "sqlite:///./insta_agent.db"
    SQLALCHEMY_ECHO: bool = True

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # JWT & Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Social Media APIs
    INSTAGRAM_CLIENT_ID: Optional[str] = None
    INSTAGRAM_CLIENT_SECRET: Optional[str] = None
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:8000/auth/instagram/callback"
    INSTAGRAM_GRAPH_API_VERSION: str = "v21.0"
    INSTAGRAM_DEMO_MODE: bool = True
    INSTAGRAM_OAUTH_SCOPES: str = (
        "instagram_basic,instagram_content_publish,"
        "instagram_manage_insights,pages_show_list"
    )
    REDIRECT_URI: Optional[str] = None
    FRONTEND_URL: str = "http://localhost:3000"

    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_REDIRECT_URI: str = "http://localhost:8000/auth/linkedin/callback"

    TWITTER_CLIENT_ID: Optional[str] = None
    TWITTER_CLIENT_SECRET: Optional[str] = None
    TWITTER_REDIRECT_URI: str = "http://localhost:8000/auth/twitter/callback"

    # LLM Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"

    # Image Generation
    STABLE_DIFFUSION_BASE_URL: str = "http://127.0.0.1:7860"
    STABLE_DIFFUSION_TIMEOUT_SECONDS: int = 180
    STABLE_DIFFUSION_NEGATIVE_PROMPT: str = (
        "blurry, distorted, low quality, text artifacts, watermark, duplicate elements, extra limbs"
    )

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    class Config:
        env_file = str(Path(__file__).resolve().parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

    @property
    def backend_env_path(self) -> Path:
        return Path(__file__).resolve().parent / ".env"

    @property
    def instagram_redirect_uri(self) -> str:
        return self.REDIRECT_URI or self.INSTAGRAM_REDIRECT_URI

    @property
    def instagram_graph_api_base_url(self) -> str:
        version = (self.INSTAGRAM_GRAPH_API_VERSION or "v21.0").strip()
        return f"https://graph.facebook.com/{version}"

    @staticmethod
    def _has_real_value(value: Optional[str]) -> bool:
        if value is None:
            return False

        normalized = value.strip()
        if not normalized:
            return False

        return normalized.lower() not in PLACEHOLDER_ENV_VALUES

    @staticmethod
    def _is_valid_instagram_app_id(value: Optional[str]) -> bool:
        if not value:
            return False

        return value.strip().isdigit()

    @property
    def instagram_app_id_valid(self) -> bool:
        return self._is_valid_instagram_app_id(self.INSTAGRAM_CLIENT_ID)

    @property
    def instagram_oauth_configured(self) -> bool:
        return (
            self.instagram_app_id_valid
            and self._has_real_value(self.INSTAGRAM_CLIENT_SECRET)
        )

    @property
    def instagram_connection_mode(self) -> str:
        if self.instagram_oauth_configured:
            return "oauth"
        if self.INSTAGRAM_DEMO_MODE:
            return "demo"
        return "disabled"

    def update_instagram_oauth_settings(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None,
        graph_api_version: Optional[str] = None,
        demo_mode: bool = False,
    ) -> None:
        normalized_client_id = (client_id or "").strip()
        normalized_client_secret = (client_secret or "").strip()
        normalized_redirect_uri = (redirect_uri or self.instagram_redirect_uri).strip()
        normalized_graph_version = (graph_api_version or self.INSTAGRAM_GRAPH_API_VERSION or "v21.0").strip()

        if not self._has_real_value(normalized_client_id):
            raise ValueError("Valid INSTAGRAM_CLIENT_ID required.")

        if not normalized_client_id.isdigit():
            raise ValueError("INSTAGRAM_CLIENT_ID must be a numeric App ID.")

        if not self._has_real_value(normalized_client_secret):
            raise ValueError("Valid INSTAGRAM_CLIENT_SECRET required.")

        updates = {
            "INSTAGRAM_CLIENT_ID": normalized_client_id,
            "INSTAGRAM_CLIENT_SECRET": normalized_client_secret,
            "INSTAGRAM_REDIRECT_URI": normalized_redirect_uri,
            "INSTAGRAM_GRAPH_API_VERSION": normalized_graph_version,
            "INSTAGRAM_DEMO_MODE": "True" if demo_mode else "False",
        }

        self._write_env_updates(self.backend_env_path, updates)

        for key, value in updates.items():
            os.environ[key] = value

        object.__setattr__(self, "INSTAGRAM_CLIENT_ID", normalized_client_id)
        object.__setattr__(self, "INSTAGRAM_CLIENT_SECRET", normalized_client_secret)
        object.__setattr__(self, "INSTAGRAM_REDIRECT_URI", normalized_redirect_uri)
        object.__setattr__(self, "INSTAGRAM_GRAPH_API_VERSION", normalized_graph_version)
        object.__setattr__(self, "INSTAGRAM_DEMO_MODE", demo_mode)

    @staticmethod
    def _write_env_updates(env_path: Path, updates: dict[str, str]) -> None:
        env_path.parent.mkdir(parents=True, exist_ok=True)
        existing_lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
        new_lines: list[str] = []
        updated_keys: set[str] = set()

        for raw_line in existing_lines:
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                new_lines.append(raw_line)
                continue

            key, _ = raw_line.split("=", 1)
            normalized_key = key.strip()
            if normalized_key in updates:
                new_lines.append(f"{normalized_key}={updates[normalized_key]}")
                updated_keys.add(normalized_key)
            else:
                new_lines.append(raw_line)

        for key, value in updates.items():
            if key not in updated_keys:
                new_lines.append(f"{key}={value}")

        env_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


_load_workspace_root_env()
settings = Settings()
