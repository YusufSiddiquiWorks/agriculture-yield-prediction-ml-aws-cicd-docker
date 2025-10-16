#!/bin/bash
set -e

echo "🛑 Stopping old container (if any)..."

CONTAINER_ID=$(docker ps -qf "ancestor=yswork/music-customer-churn-prediction-ml:aws_prod_v1")

if [ -n "$CONTAINER_ID" ]; then
  docker rm -f "$CONTAINER_ID" || true
  echo "✅ Previous container stopped."
else
  echo "ℹ️ No container found — skipping stop step."
fi

exit 0