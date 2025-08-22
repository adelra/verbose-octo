# verbose-octo

This project is a machine learning application that uses YOLOv8 for object detection. It provides a FastAPI service to make predictions on images.

## Requirements

*   Python 3.11
*   Dependencies are listed in the `pyproject.toml` file.

## Running the API

To build and run the API, you need to have Docker and Docker Compose installed.

1.  **Build and run the container:**

    ```bash
    docker-compose up --build
    ```

    The API will be available at `http://localhost:8000`.

## API Usage

You can send a POST request to the `/predict` endpoint with an image file to get the predictions.

**Example using `curl`:**

```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/predict/
```

**Example Response:**

```json
{
  "predictions": [
    {
      "x1": 100.0,
      "y1": 200.0,
      "x2": 300.0,
      "y2": 400.0,
      "label": "cat",
      "confidence": 0.95
    }
  ]
}
```

## Deployment Considerations

When deploying this model to a production environment, you should consider the following:

*   **Model Storage:** The model is currently downloaded at startup. For a production environment, you can store the model in a more persistent way, for example, in a cloud storage bucket.
*   **Scalability:** The current setup runs a single container. To handle more traffic, you can consider deploying the application to a scalable platform like Kubernetes.
*   **Monitoring:** You can consider adding monitoring to the API
*   **Security:** In prod envs we should secure the API by adding authentication and authorization.

## Running the Tests

To run the tests, you can use the `tester` service defined in the `docker-compose.yml` file.

```bash
docker-compose run tester
```

### Model Selection: Why YOLO?

For the task of object detection in a retail environment, YOLO (You Only Look Once) stands out as an excellent choice for its performance characteristics. Below is why: 

**1. Real-Time Performance:**

YOLO is famous for its speed. It processes entire images in a single forward pass, making it one of the fastest object detection models available. In a retail setting, this is crucial for applications like real-time inventory tracking, shelf monitoring, or customer behavior analysis.

**2. High Accuracy:**

While being fast, YOLO also maintains a high level of accuracy. It makes fewer background errors compared to other models. This is because it sees the entire image at once, giving it global context for the objects it's detecting.

**3. Good Generalization:**

YOLO models are known to generalize well from training data to new, unseen data. This is a valuable trait in a retail environment where lighting conditions, product placement, and camera angles can vary.

**4. Open-Source and Actively Developed:**

YOLO is an open-source project with a large and active community. This means there are many resources available, and the model is constantly being improved upon with new versions that offer better performance and features.

**5. Unified and Simple Framework:**

YOLO's architecture is a single neural network for the entire object detection pipeline. This makes it simpler to train and deploy compared to two-stage detectors that have separate components for region proposals and object classification.

While YOLO can sometimes struggle with detecting very small objects, its overall balance of speed, accuracy, and ease of use makes it a compelling choice for the challenges presented in this technical test.
