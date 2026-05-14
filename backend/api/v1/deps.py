
#python modules
from typing import Optional
from uuid import UUID

#my modules
from api.v1.schemas.user_auth import TokenResponse
import core.secure as secure
from api.v1.database.session import get_db
from api.v1.database.models.user import UserTable 

#fast api moduless
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyCookie

#alchemy modules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

bearer_scheme = HTTPBearer(auto_error=False)
cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)


async def get_current_user(
        bearer_credentials : Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
        cookie_token : str = Depends(cookie_scheme),
        db : AsyncSession = Depends(get_db)
        )->UserTable:
    
    token : Optional[None] = None  

    if bearer_credentials:
        token = bearer_credentials.credentials
    if cookie_token:
        token = cookie_token 

    if not token: 
        raise HTTPException(status_code=401, detail="Not authenticated")


    payload = secure.decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token missing user id")
    

    result = await db.execute(select(UserTable).where(UserTable.id == UUID(user_id))) 
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="user not found or inactive")

    return user








