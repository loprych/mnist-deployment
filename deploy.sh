#!/bin/bash

check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

echo "=== Starting Deployment Process ==="

echo "=== Building and running train stage ==="
cd train || exit
docker build -t mnist-train:latest .
check_status "Failed to build mnist-train Docker image."
docker run --rm -v "$(pwd)/data:/data" mnist-train:latest
check_status "Failed to run mnist-train Docker container."
cd ..

echo "=== Building and running eval stage ==="
cd eval || exit
docker build -t mnist-eval:latest .
check_status "Failed to build mnist-eval Docker image."
docker run --rm -v "$(pwd)/../train/data/mnist_model_improved.keras:/data/mnist_model_improved.keras" mnist-eval:latest
check_status "Failed to run mnist-eval Docker container."
cd ..

echo "=== Building and running serve stage ==="
cd serve || exit
docker build -t mnist-serve:latest .
check_status "Failed to build mnist-serve Docker image."
docker run -d -p 3002:3002 -v "$(pwd)/../train/data/mnist_model_improved.keras:/data/mnist_model_improved.keras" mnist-serve:latest
check_status "Failed to run mnist-serve Docker container."
cd ..

echo "Serve endpoint is running in the background at http://localhost:3002"

echo "=== Active Docker Containers ==="
docker ps

echo "=== Deployment Complete ==="
