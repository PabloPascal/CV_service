from fastapi import FastAPI 
from api.v1.routes.video_routs import router 
import uvicorn 


app = FastAPI()
app.include_router(router)


@app.get("/")
async def HelloPage():
    return "Hello User!!!" 



if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True)


