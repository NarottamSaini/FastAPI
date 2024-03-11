from fastapi import APIRouter
from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from fastapi.params import Depends
from ..import schemas
from ..import models
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter(tags=['Seller'],
                   prefix="/seller")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@router.post('/', response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db:Session=Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(username = request.username, email = request.email, password = hashedpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
