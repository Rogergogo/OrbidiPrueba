from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from schemas.location import (
    Location,
    LocationCreate,
    LocationCategoryReviewed,
)
from database import get_db
from crud.location import (
    create_location,
    get_locations,
    get_location,
    get_suggestions,
    update_location_review,
)

router = APIRouter()


@router.post("/locations/", name="Create Locations", response_model=Location)
def create_location_endpoint(location: LocationCreate, db: Session = Depends(get_db)):
    """
    Create the Location and location_category records for every location-category combination
    - **name**: Name of the location.
    - **longitude**: Longitude of the location.
    - **latitude**: Latitude of the location.
    - **category_ids**: List of category IDs associated with the location.
    """
    return create_location(db=db, location=location)


@router.get("/locations/", name="List Locations", response_model=List[Location])
def get_locations_endpoint(
    skip: int = Query(0, description="Number of records to skip.", example=0),
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Read a list of locations with pagination.

    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.
    """
    locations = get_locations(db, skip=skip, limit=limit)
    return locations


@router.get("/locations/{location_id}", name="Get Location", response_model=Location)
def get_location_endpoint(location_id: int, db: Session = Depends(get_db)):
    """
    Read a specific location by ID.

    - **location_id**: ID of the location to read.
    """
    db_location = get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router.put(
    "/reviews/{location_id}/{category_id}",
    name="Update location review",
    response_model=LocationCategoryReviewed,
)
def update_review_endpoint(
    location_id: int,
    category_id: int,
    db: Session = Depends(get_db),
):
    return update_location_review(location_id, category_id, db)


@router.get(
    "/suggestions/",
    name="Location suggestions",
    response_model=List[LocationCategoryReviewed],
)
def get_suggestions_endpoint(db: Session = Depends(get_db)):
    """
    Return suggestions of locations , prioritizing those never reviewed and older (30 days)
    """
    return get_suggestions(db)
