from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="ozon-api-service", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    api_prefix: str = "/api"

    mysql_host: str = Field(default="182.92.251.60", alias="MYSQL_HOST")
    mysql_port: int = Field(default=13306, alias="MYSQL_PORT")
    mysql_database: str = Field(default="ozon-service", alias="MYSQL_DATABASE")
    mysql_user: str = Field(default="root", alias="MYSQL_USER")
    mysql_password: str = Field(default="ShT202488@", alias="MYSQL_PASSWORD")

    redis_host: str = Field(default="182.92.251.60", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: str | None = Field(default="zhyt#666888", alias="REDIS_PASSWORD")

    ozon_base_url: str = Field(default="https://api-seller.ozon.ru", alias="OZON_BASE_URL")
    ozon_credential_ttl_seconds: int = Field(default=3600, alias="OZON_CREDENTIAL_TTL_SECONDS")
    ozon_timeout_seconds: float = Field(default=60.0, alias="OZON_TIMEOUT_SECONDS")
    ozon_category_tree_ttl_seconds: int = Field(default=86400, alias="OZON_CATEGORY_TREE_TTL_SECONDS")
    ozon_category_attributes_ttl_seconds: int = Field(default=43200, alias="OZON_CATEGORY_ATTRIBUTES_TTL_SECONDS")
    ozon_attribute_values_ttl_seconds: int = Field(default=21600, alias="OZON_ATTRIBUTE_VALUES_TTL_SECONDS")
    import_task_poller_enabled: bool = Field(default=True, alias="IMPORT_TASK_POLLER_ENABLED")
    import_task_poller_interval_seconds: int = Field(default=10, alias="IMPORT_TASK_POLLER_INTERVAL_SECONDS")
    import_task_poller_batch_size: int = Field(default=50, alias="IMPORT_TASK_POLLER_BATCH_SIZE")
    import_task_poller_min_age_seconds: int = Field(default=300, alias="IMPORT_TASK_POLLER_MIN_AGE_SECONDS")
    app_activation_admin_token: str = Field(default="", alias="APP_ACTIVATION_ADMIN_TOKEN")
    cors_allow_origins: str = Field(
        default="https://localhost,http://localhost,http://localhost:5173,http://127.0.0.1:5173,capacitor://localhost,https://www.stgpu.com",
        alias="CORS_ALLOW_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
