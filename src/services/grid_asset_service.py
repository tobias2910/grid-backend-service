"""Grid asset related services."""
from typing import List

from beanie import PydanticObjectId
from beanie.odm.operators.find.geospatial import Near
from fastapi import HTTPException, status

from src.models.grid_asset_model import ContactInformation, GeoData, GridAsset
from src.schemas.grid_asset_schema import DBGridAsset


class GridAssetService:
    """Services for managing grid assets in the database."""

    async def obtain_all_assets(self, limit: int, skip: int) -> List[GridAsset]:
        """Get the specified article from the database.

        Args:
            limit: The maximum number of items to obtain.
        Returns:
            A list of all grid assets
        """
        assets = await GridAsset.all(limit=limit, skip=skip).sort(GridAsset.name).to_list()
        return assets

    async def obtain_asset(self, id: PydanticObjectId) -> GridAsset:
        """Obtain the specified asset information.

        Args:
            id: The ID of the grid asset to obtain.
        Returns:
            The grid asset that matches the ID.
        Raises:
            HTTPException: Raised, when no asset is matching the ID.
        """
        asset = await GridAsset.get(document_id=id)
        if not asset:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No asset matching the provided ID")
        return asset

    async def obtain_nearly_assets(self, lat: float, lon: float, max_distance: int) -> List[GridAsset]:
        """Obtain assets that are near to the specified coordinates.

        Args:
            lat: The latitude of the coordinates to find nearly assets.
            lon: The longitude of the coordinates to find nearly assets.
            max_distance: The max range in meters to find nearly assets.
        Returns:
            The list of grid assets that are within the specified area.
        Raises:
            HTTPException: Raised, when no assets are available within the specified area.
        """
        assets = GridAsset.find(Near(GridAsset.geo, lat, lon, max_distance=max_distance))
        if not assets:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No assets within the specified range found")
        result = await assets.to_list()
        return result

    async def create_asset(
        self, name: str, status: bool, first_name: str, last_name: str, mail: str, lat: float, lon: float
    ) -> DBGridAsset:
        """Create a new asset.

        Args:
            name: The name of the asset.
            status: The status of the asset (active / not-active).
            first_name: The first name of the contact person.
            last_name: The last name of the contact person.
            mail: The mail address of the contact person.
            lat: The latitude of the grid asset.
            lon: The longitude of the grid asset.
        """
        asset = GridAsset(
            name=name,
            status=status,
            contact_information=ContactInformation(first_name=first_name, last_name=last_name, mail=mail),
            geo=GeoData(coordinates=(lat, lon)),
        )
        await asset.insert()
        return asset
