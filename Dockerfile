FROM python:3.10-slim-buster AS builder

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    swig \
    libssl-dev \
    python3-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
