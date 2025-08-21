FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1

# Install uv
RUN pip install uv

COPY pyproject.toml .

# Use uv to install dependencies
RUN uv pip install --system --no-cache-dir .

COPY ./src ./src

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
