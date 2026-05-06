from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from ml_model.model_response import predict
import os 
import shutil
import time 


SAVE_DIR = Path("video_saves")
RESPONSE_DIR = Path("runs/detect/fixed_output")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


router = APIRouter()


filename: str = None 


@router.get("/video/{filename}")
async def get_content(filename : str):
    file_path = RESPONSE_DIR / filename

    print(f"FILE_RESPONSE_PATH: {file_path}")

    # if not file_path.exists(): 
    #     raise HTTPException(status_code=404, detail="file not found")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename,
        headers={"Content-Disposition": "inline"}
    )





@router.post("/video")
async def upload_video(file : UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
        status_code=400, 
        detail=f"Неподдерживаемый формат видео. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    print(f" file size = {file.size}") 
    if file.size / 1024 > 3*1024:
        raise HTTPException(status_code=400, detail="too big size")   

    print(f"EXTENSION = {ext}")

    global filename 
    
    filename = time.clock_gettime(time.CLOCK_REALTIME).hex() + ext
    #filename = "video_loaded" + ext
    file_path = SAVE_DIR / filename 
    
    print(f"FILENAME: {filename}")
    
    try:   
        with file_path.open("wb") as buffer: 
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения: {e}")

    finally:
        await file.close()


    return {"message": "Видео загружено", "filename": filename, "path": str(file_path)}


print(f"FILENAME: {filename}")



@router.get("/response")
async def response_model()-> dict:
    file_path = SAVE_DIR / filename
    await predict(file_path)
    return {"response" : f"FILE_PATH: {filename}"}



@router.get("/response/{filepath}")
async def response_model(filepath)-> dict:
    file_path = SAVE_DIR / filepath
    await predict(file_path)
    return {"response" : f"FILE_PATH: {filename}"}



