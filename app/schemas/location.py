from datetime import datetime
from pydantic import BaseModel, Field, conlist
from typing import List, Optional
from schemas.category import Category


class LocationBase(BaseModel):
    """
    Location model Base Dataclass
    """

    name: str = Field(example="Central Park", description="Name of the location.")
    longitude: str = Field(
        example="40.785091", description="Longitude of the location."
    )
    latitude: str = Field(example="-73.968285", description="Latitude of the location.")


class LocationCreate(LocationBase):
    """
    Create location model DataClass
    """

    category_ids: conlist(int, min_length=1) = Field(
        example="[x,xx,xxx,xxx,xxx]",
        description="List of category IDs associated with the location.",
    )


class Location(LocationBase):
    """
    location model Main Dataclass
    """

    id: int
    categories: List[Category]

    class Config:
        orm_mode = True


class LocationCategoryReviewedBase(BaseModel):
    """
    location_category_reviewed model Base Dataclass
    """

    reviewed_at: Optional[bool] = False
    reviewed_at: Optional[datetime] = None


class LocationReviewResponse(BaseModel):
    id: int
    name: str
    latitude: str
    longitude: str

    class Config:
        orm_mode = True


class CategoryReviewResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    """
    location_category_reviewed model create db DataClass
    """

    location_id: int
    category_id: int


class LocationCategoryReviewed(LocationCategoryReviewedBase):
    """
    location_category_reviewed  model Main DataClass
    """

    location: LocationReviewResponse
    category: CategoryReviewResponse

    class Config:
        orm_mode = True
