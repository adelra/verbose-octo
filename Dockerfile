FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

COPY pyproject.toml .

RUN pip install uv
RUN pip install --no-cache-dir .[dev] jupyterlab

COPY ./src ./src
COPY ./tests ./tests
COPY ./notebooks ./notebooks


EXPOSE 8000
EXPOSE 8888

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
