from fastapi import FastAPI 
from contextlib import asynccontextmanager
 
from api.v1.routes.video_routes import router 
from api.v1.routes.user_routes import user_router
from api.v1.database.session import engine, Base
import uvicorn 


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("Application starting...")
    # Создать таблицы, если их ещё нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables ensured.")
    yield  # здесь приложение работает
    # --- Shutdown ---
    print("Application shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(user_router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8111, reload=True)


