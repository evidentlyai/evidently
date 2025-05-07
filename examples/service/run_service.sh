docker run -p 8000:8000 \
  -v $(pwd)/workspace:/app/workspace \
  --name evidently-service \
  --detach \
  evidently/evidently-service:latest