from ultralytics import YOLO
import pytest
from fastapi.testclient import TestClient
from src.api import app
import io
from PIL import Image

client = TestClient(app)


def test_load_model():
    """
    Tests that the YOLOv8 model can be loaded.
    """
    try:
        YOLO("yolov8n.pt")
    except Exception as e:
        pytest.fail(f"Failed to load YOLOv8 model: {e}")


def test_predict_endpoint():
    """
    Tests the /predict/ endpoint.
    """
    # Create a dummy image
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    response = client.post(
        "/predict/", files={"file": ("test.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert isinstance(data["predictions"], list)
