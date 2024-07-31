from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.location import Location, LocationCategoryReviewed, location_category
from models.category import Category
from schemas.location import LocationCreate


def get_location(db: Session, location_id: int) -> Optional[Location]:
    return db.query(Location).filter(Location.id == location_id).first()


def get_locations(db: Session, skip: int = 0, limit: int = 10) -> List[Location]:
    return db.query(Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: LocationCreate) -> Location:
    try:
        # Begin atomic transaction

        db.begin()
        # create Location
        db_location = Location(
            name=location.name,
            longitude=location.longitude,
            latitude=location.latitude,
        )
        db.add(db_location)
        db.commit()
        db.refresh(db_location)

        # Validate category_ids provided
        if location.category_ids:
            count_valid_ids = (
                db.query(Category)
                .filter(Category.id.in_(location.category_ids))
                .count()
            )
            if count_valid_ids != len(location.category_ids):
                raise HTTPException(
                    status_code=400, detail="Invalid category IDs provided"
                )

        # Create location_category without reviewed_at
        for category_id in location.category_ids:
            db_review = LocationCategoryReviewed(
                location_id=db_location.id, category_id=category_id, reviewed=False
            )
            db.execute(
                location_category.insert().values(
                    location_id=db_location.id, category_id=category_id
                )
            )
            db.add(db_review)

        db.commit()
        db.refresh(db_location)
        return db_location
    except Exception as e:
        # Capture exception , Rollback transaction
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e


def update_location_review(
    location_id: int,
    category_id: int,
    db: Session,
):
    review = (
        db.query(LocationCategoryReviewed)
        .filter(
            LocationCategoryReviewed.location_id == location_id,
            LocationCategoryReviewed.category_id == category_id,
        )
        .first()
    )

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.reviewed = True
    review.reviewed_at = datetime.now()

    db.commit()
    db.refresh(review)

    return review


def get_suggestions(db: Session):
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Query for reviewed entries older than 30 days or never reviewed
    suggestions = (
        db.query(LocationCategoryReviewed)
        .join(Location)
        .join(Category)
        .filter(
            (LocationCategoryReviewed.reviewed == False)
            | (LocationCategoryReviewed.reviewed_at < thirty_days_ago)
        )
        .order_by(
            LocationCategoryReviewed.reviewed, LocationCategoryReviewed.reviewed_at
        )
        .limit(10)
        .all()
    )

    if not suggestions:
        raise HTTPException(status_code=404, detail="No suggestions found")

    return suggestions
