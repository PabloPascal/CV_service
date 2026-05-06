
from ultralytics import YOLO 
import asyncio



model = YOLO('yolov8n.pt')


async def predict(filename : str):

    loop = asyncio.get_event_loop()

    exec = lambda: model.predict(
        source=filename,
        project="runs/detect",
        name="fixed_output",
        save=True,
        exist_ok=True,
        conf=0.25
        )

    results = await loop.run_in_executor(None, exec)



    


