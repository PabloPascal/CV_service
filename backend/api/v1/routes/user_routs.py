#my modules
from api.v1.database.session import get_db 
from api.v1.database.models.user import UserTable
from api.v1.schemas.user_auth import UserRegister, TokenResponse, UserLogin
import core.secure as secure

#sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

#fastapi
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse

user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.post("/user_register")
async def register(
    user_in : UserRegister,
    db : AsyncSession = Depends(get_db)
    )->JSONResponse:
    
    result_user = db.execute(select(UserTable).where(UserTable.username == user_in.username))

    if(result_user != None):
        raise HTTPException(status_code=401, detail="user already exist")

    hash_password = secure.get_password_hash(user_in.password)
    new_user_table = UserTable(user_in.username, hash_password)

    db.add(new_user_table)
    await db.commit()
    await db.refresh(new_user_table)

    access_token = secure.create_access_token(new_user_table.id)
    refresh_token = secure.create_refresh_token(new_user_table.id)

    response = JSONResponse(
        content={"message" : "user registered"},
        status_code=200
    )

#    _set_refresh_cookie(response, refresh_token)
    return response



@user_router.post("/user_login", response_model=TokenResponse)
async def login(
    user_in : UserLogin,
    db : AsyncSession = Depends(get_db)
    ):

    result = await db.execute(select(UserTable).where(UserTable.username) == user_in.username)
    user_db = result.scalar_or_none()

    if not user_db or not secure.verify_password(user_in.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="failed to login")

    access_token = secure.create_access_token(user_db.id)
    refresh_token = secure.create_refresh_token(user_db.id)

    token = TokenResponse({"token" : access_token, "token_type" : "bearer"})

    return token 

    
