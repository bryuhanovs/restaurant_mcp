from functools import lru_cache
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout_seconds: float = 30
    db_statement_timeout_ms: int = 5000
    db_max_rows: int = 500

    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8000
    mcp_env: Literal["development", "production"] = "development"
    mcp_api_key: str = ""
    mcp_allowed_hosts: str = ""
    mcp_allowed_origins: str = ""
    forwarded_allow_ips: str = ""

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("db_pool_size", "db_max_overflow", "db_statement_timeout_ms", "db_max_rows")
    @classmethod
    def must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("must be positive")
        return value

    @property
    def allowed_hosts(self) -> list[str]:
        return _split_csv(self.mcp_allowed_hosts)

    @property
    def allowed_origins(self) -> list[str]:
        return _split_csv(self.mcp_allowed_origins)

    @property
    def exposes_network(self) -> bool:
        return self.mcp_host not in _LOCAL_HOSTS or self.mcp_env == "production"

    @model_validator(mode="after")
    def require_network_guards(self) -> "Settings":
        if not self.exposes_network:
            return self
        if not self.mcp_api_key:
            raise ValueError("MCP_API_KEY is required when the server is reachable beyond localhost")
        if not self.allowed_hosts:
            raise ValueError("MCP_ALLOWED_HOSTS is required when the server is reachable beyond localhost")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
