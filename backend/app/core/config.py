from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Modular IVR Platform"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite:///./ivr.db"
    cors_origins: str = "http://localhost:5173"

    acs_connection_string: str = ""
    acs_source_phone_number: str = "+15555550123"
    acs_callback_base_url: str = "http://localhost:8000"
    acs_use_mock: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
