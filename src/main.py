"""Initializes the App with the provided configurations and middleware."""
import motor
import sentry_sdk
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.config.settings import settings
from src.models.models import __beanie_models__
from src.routers.api import api_router

# Initialize the app
app = FastAPI()

# Initialize the Sentry client
sentry_sdk.init(
    dsn="https://a5dc106a53214ccc93b2ecabb217ab86@o1381965.ingest.sentry.io/4504592317415424",
    traces_sample_rate=settings.SENTRY_TRACE_SAMPLE_RATE,
)

# Add the middlewares to the chain
app.add_middleware(GZipMiddleware)

# Attach all the routers
app.include_router(api_router)


@app.on_event("startup")
async def initalize_mongo() -> None:
    """Initialize the mongo client on startup."""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_URL)
    await init_beanie(database=client[settings.MONGO_DB_DATABASE], document_models=__beanie_models__)  # type: ignore
