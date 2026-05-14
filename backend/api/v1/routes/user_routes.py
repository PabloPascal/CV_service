#my modules
from api.v1.database.session import get_db 
from api.v1.database.models.user import UserTable
from api.v1.schemas.user_auth import UserRegister, TokenResponse, UserLogin
from api.v1.schemas.user import UserOut
import core.secure as secure
from api.v1.deps import get_current_user

#sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

#fastapi
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse

user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.get("/")
async def HelloPage():
    return "Hello User FROM USER_ROUTES!!!" 




@user_router.post("/user_register")
async def register(
    user_in : UserRegister,
    db : AsyncSession = Depends(get_db)
    )->JSONResponse:
    
    result_user = await db.execute(select(UserTable).where(UserTable.username == user_in.username))
    existing_user = result_user.scalar_one_or_none()


    if existing_user is not None:
        raise HTTPException(status_code=401, detail="user already exist")

    hash_password = secure.get_password_hash(user_in.password)
    new_user_table = UserTable(username=user_in.username, hashed_password=hash_password)

    db.add(new_user_table)
    await db.commit()
    await db.refresh(new_user_table)

    access_token = secure.create_access_token(str(new_user_table.id))
    refresh_token = secure.create_refresh_token(str(new_user_table.id))

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

    result = await db.execute(
        select(UserTable).where(UserTable.username == user_in.username)
        )
    user_db = result.scalar_one_or_none()

    if not user_db or not secure.verify_password(user_in.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="failed to login")

    access_token = secure.create_access_token(str(user_db.id))
    refresh_token = secure.create_refresh_token(str(user_db.id))

    token = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

    return token 

    

@user_router.get("/get_me", response_model=UserOut)
async def read_current_user(
    current_user: UserTable = Depends(get_current_user)
):
    return current_user


