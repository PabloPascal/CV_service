from pydantic import BaseModel
from uuid import UUID 
from datetime import datetime

class UserOut(BaseModel):
    id : UUID 
    username : str 
    is_active : bool 
    created_at : datetime

    class Config:
        from_attributes = True


