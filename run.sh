#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Levels.fyi Compensation Validation System v3.0       ║"
echo "║                   Starting Services...                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p data models logs

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
fi

# Build and start services
echo -e "${GREEN}📦 Building and starting Docker containers...${NC}"
docker-compose up -d --build

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check API health
echo -e "${GREEN}🔍 Checking service health...${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ API is healthy${NC}"
else
    echo -e "${RED}❌ API health check failed${NC}"
fi

# Initialize database
echo -e "${GREEN}🗄️  Initializing database...${NC}"
docker-compose exec api python scripts/init_db.py

# Train models
echo -e "${GREEN}🤖 Training ML models...${NC}"
docker-compose exec api python scripts/train_models.py

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗"
echo -e "║                    SYSTEM IS READY!                            ║"
echo -e "╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Access your services:"
echo -e "  📡 API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  📊 Dashboard:         ${GREEN}http://localhost:8501${NC}"
echo -e "  📈 Metrics:           ${GREEN}http://localhost:9090${NC}"
echo ""
echo -e "Test with curl:"
echo -e "  ${YELLOW}curl http://localhost:8000/${NC}"
echo ""
echo -e "Stop services: ${YELLOW}docker-compose down${NC}"
echo -e "View logs:     ${YELLOW}docker-compose logs -f${NC}"