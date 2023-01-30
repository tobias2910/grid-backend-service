"""Reads and provides the environment variables as a dict."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Reads all the environment variables."""

    # Mongo DB settings
    MONGO_DB_URL: str
    MONGO_DB_DATABASE: str

    # Sentry settings
    SENTRY_DSN: str
    SENTRY_TRACE_SAMPLE_RATE: float

    class Config(BaseSettings.Config):
        """Set the settings."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
