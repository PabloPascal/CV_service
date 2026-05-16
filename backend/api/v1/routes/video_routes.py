#fastapi
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse

#my modules
from api.v1.database.models.user import UserTable
from api.v1.deps import get_current_user
from api.v1.ml_model.model_response import predict
from api.v1.deps import get_storage, Storage
from api.v1.database.session import get_db

#others
from pathlib import Path
import os 
import shutil
import time 



SAVE_DIR = Path("video_saves")
RESPONSE_DIR = Path("runs/detect/fixed_output")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


router = APIRouter()


filename: str = ""

#============================================
# Get Contnet like Video
#============================================
@router.get("/video/{filename}")
def get_content(filename : str):
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




#============================================
#Upload video
#============================================
@router.post("/video")
async def upload_video(file : UploadFile = File(...)):

    if file.size is None:
        raise HTTPException(status_code=400, detail="dont have content")
    
    if file.filename is None:
        raise HTTPException(status_code=400, detail="need the name")

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
    
    filename = time.time_ns().to_bytes(8, 'big').hex() + ext
    #filename = time.clock_gettime(time.CLOCK_REALTIME).hex() + ext
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





#============================================
# get Response from model 
#============================================
@router.get("/response")
async def response_YOLOmodel()-> dict:
    file_path = SAVE_DIR / filename
    await predict(str(file_path))
    return {"response" : f"FILE_PATH: {filename}"}






#============================================
#Get Response and u can input filepath
#============================================
@router.get("/response/{filepath}")
async def response_model(filepath)-> dict:
    file_path = SAVE_DIR / filepath
    await predict(file_path)
    return {"response" : f"FILE_PATH: {filename}"}




#============================================
#Upload video and save it to db (Authenticator)(S3)
#============================================
@router.post("/upload_and_save_video")
async def upload_save(video : UploadFile = File(...), 
                      current_user : UserTable = Depends(get_current_user),
                      db : UserTable = Depends(get_db),
                      storage : Storage = Depends(get_storage)
                      ):
    
    if video.filename is None:
        raise HTTPException(status_code=400, detail=f"file must be named")

    ext = Path(video.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail=f"unsupported extension: {ext}")


    object_name = f"{current_user.id}/{time.time_ns().to_bytes(8, 'big').hex() + ext}"

    try:
        await storage.upload_object(
            storage.bucket_input,
            object_name,
            video.file,
            length=video.size
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"failed to upload data to storage: {ex}")


    return JSONResponse(
        content={"message": "Video uploaded", "object_name": object_name},
        status_code=201
    )



"""request_id": str(new_request.id)"""
