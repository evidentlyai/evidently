docker run -p 8000:8000 \
  -v $(pwd)/workspace:/app/workspace \
  --name evidently-service \
  --detach \
  evidently/evidently-service:0.3.3-1a77ad6e-dirty