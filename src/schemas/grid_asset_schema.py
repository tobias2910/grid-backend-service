"""Grid asset schema."""
from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from src.models.grid_asset_model import GridAsset


class CreateGridAsset(BaseModel):
    """Base model for a grid asset."""

    name: str = Field(example="Grid Asset #102")
    status: bool = Field(example=True)
    first_name: str = Field(example="Tobias")
    last_name: str = Field(example="Caliskan")
    mail: str = Field(example="tobiascaliskan@gmail.org")
    lat: float = Field(example=24.345, min=-90, max=90)
    lon: float = Field(example=33.34334, min=-180, max=180)


class DBGridAsset(GridAsset):
    """The response model for the created asset."""

    _id: PydanticObjectId
