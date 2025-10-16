#!/bin/bash

set -e

TARGET_DIR="/home/ubuntu/app_agriculture_yield_prediction_ml"

if [ -d "$TARGET_DIR" ]; then
  echo "Deleting previous deployment directory $TARGET_DIR"
  sudo rm -rf "$TARGET_DIR"
fi
