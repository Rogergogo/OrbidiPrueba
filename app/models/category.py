from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    """
    Model representing a specific category.
    """

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    locations = relationship(
        "Location",
        secondary="location_category",
        back_populates="categories",
        doc="Locations associated with the category",
    )
    reviews = relationship("LocationCategoryReviewed", back_populates="category")
