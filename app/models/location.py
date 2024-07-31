from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Boolean
from sqlalchemy.orm import relationship

from database import Base


# Many to Many Relation
location_category = Table(
    "location_category",
    Base.metadata,
    Column(
        "location_id",
        Integer,
        ForeignKey("locations.id"),
        primary_key=True,
        doc="Identifier for the location",
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id"),
        primary_key=True,
        doc="Identifier for the category",
    ),
)


class LocationCategoryReviewed(Base):
    """
    Review Table (combination of location and category(MANY TO MANY) with review information)
    """

    __tablename__ = "location_category_reviewed"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    reviewed = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, nullable=True)

    location = relationship("Location", back_populates="reviews")
    category = relationship("Category", back_populates="reviews")


class Location(Base):
    """
    Model representing a specific location.
    """

    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    longitude = Column(String)
    latitude = Column(String)
    categories = relationship(
        "Category",
        secondary="location_category",
        back_populates="locations",
        doc="categories associated with the location",
    )
    reviews = relationship("LocationCategoryReviewed", back_populates="location")
