#!/bin/bash

# Exit on any error
set -e

# Configuration
IMAGE_NAME="asia-south1-docker.pkg.dev/gen-lang-client-0091398941/spec-validator/ai-agent:v1"
PLATFORM="linux/amd64"

echo "🚀 Starting Docker build and push process..."

# Check if gcloud is authenticated
echo "🔐 Checking gcloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: gcloud is not authenticated. Please run 'gcloud auth login' first."
    exit 1
fi

# Configure Docker to use gcloud as a credential helper
echo "🔧 Configuring Docker authentication..."
gcloud auth configure-docker asia-south1-docker.pkg.dev --quiet

# Build the Docker image for AMD64 platform
echo "🔨 Building Docker image for AMD64 platform..."
docker build --platform $PLATFORM -t $IMAGE_NAME .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker build completed successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

# Push the image to Google Artifact Registry
echo "📤 Pushing image to Google Artifact Registry..."
docker push $IMAGE_NAME

# Check if push was successful
if [ $? -eq 0 ]; then
    echo "✅ Image pushed successfully to: $IMAGE_NAME"
    echo "🎉 Build and push process completed!"
else
    echo "❌ Failed to push image to registry!"
    exit 1
fi

echo ""
echo "📋 Summary:"
echo "   Image: $IMAGE_NAME"
echo "   Platform: $PLATFORM"
echo "   Registry: Google Artifact Registry (asia-south1)" 