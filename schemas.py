from typing import Optional

from pydantic import BaseModel


class user_info_schema(BaseModel):
    name : str
    email : str
    password : str
    admin_account : Optional[str]
    photo : Optional[str]

    class Config:
        orm_mode=True

class company_info_schema(BaseModel):
    id : Optional[int]
    company : str

    class Config:
        orm_mode=True
        
class user_info_login_schema(BaseModel):
    email : str
    password : str

    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str
