#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🐳 Building Beckn Protocol Validator Docker Image...${NC}"

# Build the Docker image
docker build -t beckn-validator:latest .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
    
    echo -e "${YELLOW}🚀 Starting the container...${NC}"
    
    # Run the container
    docker run -d \
        --name beckn-validator \
        -p 7860:7860 \
        --restart unless-stopped \
        beckn-validator:latest
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Container started successfully!${NC}"
        echo -e "${GREEN}🌐 Access the application at: http://localhost:7860${NC}"
        echo -e "${YELLOW}📊 To view logs: docker logs beckn-validator${NC}"
        echo -e "${YELLOW}🛑 To stop: docker stop beckn-validator${NC}"
    else
        echo -e "${RED}❌ Failed to start container${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi 