"""The model for the grid assets."""
from typing import Tuple

from beanie import Document
from pydantic import BaseModel
from pymongo import GEOSPHERE


class GeoData(BaseModel):
    """The GeoData object."""

    type: str = "Point"
    coordinates: Tuple[float, float]


class ContactInformation(BaseModel):
    """The contact information object."""

    first_name: str
    last_name: str
    mail: str


class GridAsset(Document):
    """The Grid asset information object."""

    name: str
    status: bool
    contact_information: ContactInformation
    geo: GeoData

    class Settings:
        """The collection to store the data in the DB."""

        name = "grid_assets"
        indexes = [[("geo", GEOSPHERE)]]  # Using the geo data as the index to allow geo search
