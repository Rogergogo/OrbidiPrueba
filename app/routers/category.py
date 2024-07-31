from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.category import Category, CategoryCreate
from database import get_db
from crud.category import create_category, get_category, get_categories

router = APIRouter()


@router.post("/categories/", name="Create category", response_model=Category)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create the category
    - **name**: Name of the category.
    """
    return create_category(db=db, category=category)


@router.get("/categories/", name="List categories", response_model=List[Category])
def get_categories_endpoint(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """
    Read a list of categories with pagination.

    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.
    """
    categories = get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/categories/{category_id}", name="get category", response_model=Category)
def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    """
    Read a specific category by ID.

    - **category_id**: ID of the category to read.
    """
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
