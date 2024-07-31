from pydantic import BaseModel


class CategoryBase(BaseModel):
    """
    category model Base Dataclass
    """

    name: str


class CategoryCreate(CategoryBase):
    """
    Create category model Dataclass
    """

    pass


class Category(CategoryBase):
    """
    category model main Dataclass
    """

    id: int

    class Config:
        orm_mode = True
