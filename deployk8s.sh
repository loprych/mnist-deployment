#!/bin/bash

check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

echo "=== Starting Kubernetes Deployment Process ==="

echo "=== Applying Persistent Volume and Claim ==="
kubectl apply -f k8s/mnist-pv.yaml
check_status "Failed to apply mnist-pv.yaml."

kubectl wait --for=condition=Bound pvc/mnist-pvc --timeout=60s
check_status "PersistentVolumeClaim mnist-pvc is not bound."

echo "=== Deploying mnist-train Job ==="
kubectl apply -f k8s/mnist-train-job.yaml
check_status "Failed to deploy mnist-train job."

kubectl wait --for=condition=complete job/mnist-train --timeout=600s
check_status "mnist-train job did not complete successfully."

echo "=== Deploying mnist-eval Job ==="
kubectl apply -f k8s/mnist-eval-job.yaml
check_status "Failed to deploy mnist-eval job."

kubectl wait --for=condition=complete job/mnist-eval --timeout=600s
check_status "mnist-eval job did not complete successfully."

echo "=== Deploying mnist-serve Deployment ==="
kubectl apply -f k8s/mnist-serve-deployment.yaml
check_status "Failed to deploy mnist-serve deployment."

kubectl wait --for=condition=available deployment/mnist-serve --timeout=300s
check_status "mnist-serve deployment is not available."

echo "=== Retrieving Service Endpoint ==="
NODE_PORT=$(kubectl get svc mnist-serve-service -o=jsonpath='{.spec.ports[0].nodePort}')
check_status "Failed to retrieve mnist-serve-service NodePort."

NODE_IP=$(kubectl get nodes -o=jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
check_status "Failed to retrieve cluster node IP."

echo "=== mnist-serve Service Endpoint ==="
echo "URL: http://$NODE_IP:$NODE_PORT"

curl -s http://$NODE_IP:$NODE_PORT/health | jq
check_status "Health check failed for mnist-serve endpoint."

echo "=== Kubernetes Deployment Process Complete ==="