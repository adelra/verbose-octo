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

*   **Model Storage:** The model is currently downloaded at startup. For a production environment, you should store the model in a more persistent way, for example, in a cloud storage bucket.
*   **Scalability:** The current setup runs a single container. To handle more traffic, you should consider deploying the application to a scalable platform like Kubernetes.
*   **Monitoring:** You should set up monitoring and logging to track the performance of the model and the API.
*   **Security:** You should secure the API by adding authentication and authorization.

## Running the Tests

To run the tests, you can use the `tester` service defined in the `docker-compose.yml` file.

```bash
docker-compose run tester
```

## Running the Jupyter Notebook

Before running the notebook, ensure the COCO dataset is downloaded to your local machine:

1.  **Download COCO Dataset:**

    ```bash
    python scripts/download_coco.py
    ```

    This will download the dataset to your Hugging Face cache directory (`~/.cache/huggingface/datasets`).

2.  **Start the Jupyter Lab container:**

    ```bash
    make notebook
    ```

    This will build the Docker image (if necessary) and start Jupyter Lab, accessible via your web browser.

3.  **Access Jupyter Lab:**

    Open your web browser and navigate to `http://localhost:8888`.
    When prompted, enter `coco` as the password/token.

    You can then open and run the `coco_dataset_analysis.ipynb` notebook located in the `notebooks/` directory.