from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    price: int

class Seller(BaseModel):
    username:str
    email:str
    password: str

class DisplaySeller(BaseModel):
    username:str
    email:str
    class Config:
        orm_mode = True    

class DisplayProduct(BaseModel):
    name:str
    description:str
    seller: DisplaySeller
    class Config:
        orm_mode = True
        # from_attributes

class login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type:str

## below class will hold the username of the token holder
class TokenData(BaseModel):
    username : Optional[str] = None

        

class Temp_table(BaseModel):
    name: str
    description: str
    price: int