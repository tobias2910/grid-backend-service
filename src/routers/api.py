"""Provides a new router instance, containing all the endpoints available."""
from fastapi import APIRouter

from src.routers.v1 import grid_asset_route

api_router = APIRouter()

# Add the routers
api_router.include_router(grid_asset_route.router, prefix="/grid_assets")
