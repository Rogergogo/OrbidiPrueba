from fastapi import FastAPI

from database import engine
from models import category, location
from routers.location import router as location_router
from routers.category import router as category_router

category.Base.metadata.create_all(bind=engine)
location.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(location_router, prefix="/api/v1", tags=["locations"])
app.include_router(category_router, prefix="/api/v1", tags=["categories"])
