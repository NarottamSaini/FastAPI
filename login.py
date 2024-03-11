from fastapi import APIRouter, Depends, status, HTTPException
# from ..schemas import login
from .. import schemas, database, models
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

## below 3 variables are for JWT token
SECRET_KEY = 'db7dabc6d6fac10f49bd73e6c98d8b877b04fe441047d3c08df9c89cb05ade0c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    print("to_encode : ", to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login')
def login(request:schemas.login, db:Session=Depends(get_db)):

    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found/Invalid User")
    if not pwd_context.verify(request.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Credentails entered not correct") 
    ##Generate JWT tokens
    access_token = generate_token(data = {
        'sub': user.username
    })
    return {"access_token": access_token, "token_type": "bearer"}