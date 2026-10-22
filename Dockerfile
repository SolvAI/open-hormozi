# Optional: run OpenHormozi in Docker instead of the start scripts.
# The Playwright base image ships Chromium and its system libraries.
FROM mcr.microsoft.com/playwright/python:v1.64.0-noble

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

ENV OPENHORMOZI_DATA_DIR=/data \
    PYTHONUNBUFFERED=1
VOLUME /data
EXPOSE 8765

CMD ["python", "-m", "app", "--host", "0.0.0.0", "--port", "8765", "--no-browser"]
