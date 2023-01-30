"""All article related endpoints."""
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Path, Query, status

from src.schemas.grid_asset_schema import CreateGridAsset, DBGridAsset
from src.services.grid_asset_service import GridAssetService

grid_asset_service = GridAssetService()

router = APIRouter(tags=["Grid Asset"])


@router.get(
    "/",
    summary="Get all assets",
    description="Get all grid assets stored in the database",
    status_code=status.HTTP_200_OK,
    response_model=List[DBGridAsset],
)
async def get_all_assets(
    limit: int = Query(default=50, description="The maximum number of elements to obtain"),
    skip: int = Query(default=0, description="The number of elements to skip"),
) -> List[DBGridAsset]:
    """Endpoint for obtaining all grid assets from the database.

    Args:
        limit (int): The maximum number of elements to obtain.
        skip (int): The number of elements to skip.

    Returns:
        List[GridAsset]: The list of all grid assets in the DB.
    """
    assets = await grid_asset_service.obtain_all_assets(limit, skip)
    return assets


@router.get(
    "/{id}/",
    summary="Get the specified assets",
    description="Get the specified grid assets stored in the database",
    status_code=status.HTTP_200_OK,
    response_model=DBGridAsset,
)
async def get_asset(
    id: PydanticObjectId = Path(description="The ID of the grid asset to obtain"),
) -> DBGridAsset:
    """Endpoint for obtaining the specified grid asset from the database.

    Args:
        id (PydanticObjectId): The ID of the grid asset to obtain.

    Returns:
        List[GridAsset]: The list of all grid assets in the DB.
    """
    asset = await grid_asset_service.obtain_asset(id)
    return asset


@router.get(
    "/nearby",
    summary="Get all the nearby assets",
    description="Get all grid assets stored in the database that are within the specified range.",
    status_code=status.HTTP_200_OK,
    response_model=List[DBGridAsset],
)
async def get_nearly_assets(
    lat: float = Query(description="The latitude of the area to search for."),
    lon: float = Query(description="The latitude of the area to search for."),
    max_distance: int = Query(description="The maximum distance to search within the specified area."),
) -> List[DBGridAsset]:
    """Endpoint for obtaining nearly grid assets.

    Args:
        lat: (float): The latitude of the area to search for.
        lon: (float): The latitude of the area to search for.
        max_distance (int): The maximum distance to search within the specified area.

    Returns:
        List[GridAsset]: The list of all grid assets within the specified area.
    """
    nearly_assets = await grid_asset_service.obtain_nearly_assets(lat, lon, max_distance)
    return nearly_assets


@router.post(
    "/",
    summary="Create a new grid asset",
    description="Create a new grid asset in the database.",
    status_code=status.HTTP_201_CREATED,
    response_model=DBGridAsset,
)
async def create_asset(asset: CreateGridAsset) -> DBGridAsset:
    """Endpoint for obtaining all grid assets from the database.

    Args:
        asset (GridAsset): The maximum number of elements to obtain.

    Returns:
        GridAsset: The created grid asset.
    """
    response = await grid_asset_service.create_asset(
        asset.name,
        asset.status,
        asset.first_name,
        asset.last_name,
        asset.mail,
        asset.lat,
        asset.lon,
    )
    return response
