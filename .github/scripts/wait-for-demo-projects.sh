#!/bin/bash
# Wait for demo projects to be created by checking log output
# This script waits for the log message indicating demo projects are created

set -e

LOG_FILE="${LOG_FILE:-/tmp/evidently-ui.log}"
TIMEOUT="${TIMEOUT:-360}"  # 6 minutes default
CHECK_INTERVAL=1

echo "Waiting for demo projects to be created..."
echo "Monitoring log file: $LOG_FILE"

# Wait for log file to exist and server to start
echo "Waiting for log file to be created..."
for i in $(seq 1 60); do
  if [ -f "$LOG_FILE" ]; then
    # Also check if server is responding
    if curl -s -f http://127.0.0.1:8000/api/version > /dev/null 2>&1; then
      echo "Server is ready, monitoring logs for demo project creation..."
      break
    fi
  fi
  sleep 1
done

if [ ! -f "$LOG_FILE" ]; then
  echo "Error: Log file not found after 60 seconds"
  exit 1
fi

# Wait for the success message
START_TIME=$(date +%s)
while true; do
  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))

  if [ $ELAPSED -gt $TIMEOUT ]; then
    echo "Timeout waiting for demo projects to be created"
    exit 1
  fi

  # Check if the success message appears in the log
  # The message format is: "Demo project 'Demo project - Bikes' created successfully"
  if grep -q "Demo project.*created successfully" "$LOG_FILE" 2>/dev/null; then
    echo "Demo projects created successfully!"
    exit 0
  fi

  sleep $CHECK_INTERVAL
done
