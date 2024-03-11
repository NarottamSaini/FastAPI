from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from fastapi.params import Depends
from . import schemas
from .import models
# from pydantic import BaseModel
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# from typing import List
from passlib.context import CryptContext
from .database import get_db
from .routers import product, seller, login
# from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI(
    title="Product API",
    description="Get details of all our product @ website",
    terms_of_service="http://www.google.com",
    contact={
        "Developer name": "Narottam Saini",
        "website": "http://www.google.com",
        "email": "Narottam.Saini@ymail.com"
    },
    license_info={
        "name":"XYZ",
        "url":"http://www.google.com"
    },
    #docs_url="/documentation", redoc_url=None ## parameter for changing default url link for docs
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@app.get('/')
def home():
    return "Hello World!!"


@app.post('/temp_table', tags=['temp_table'])
def add(request:schemas.Temp_table, db: Session = Depends(get_db)):
    new_product = models.Temp_table(name=request.name, description = request.description, price = request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.delete('/temp_table/{id}')
def delete(id, db:Session = Depends(get_db)):
    product = db.query(models.Temp_table).filter(models.Temp_table.index == id).delete(synchronize_session=False)
    db.commit()
    return "Record deleted successfully"

async def common_parameters(q: str = "Narottam", skip: int = 11, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    print("commons : ", commons)
    return commons