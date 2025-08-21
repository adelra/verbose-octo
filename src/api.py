from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()

# Load the model at startup
model = YOLO("yolov8n.pt")

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    label: str
    confidence: float

class PredictionResponse(BaseModel):
    predictions: list[BoundingBox]

@app.post("/predict/", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Accepts an image file, runs inference, and returns the predictions.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    results = model(image)

    predictions = []
    for result in results:
        for box in result.boxes:
            predictions.append(
                BoundingBox(
                    x1=box.xyxy[0][0].item(),
                    y1=box.xyxy[0][1].item(),
                    x2=box.xyxy[0][2].item(),
                    y2=box.xyxy[0][3].item(),
                    label=model.names[int(box.cls)],
                    confidence=box.conf[0].item(),
                )
            )

    return PredictionResponse(predictions=predictions)
