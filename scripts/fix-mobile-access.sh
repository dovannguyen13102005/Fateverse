#!/bin/bash

# Script to fix mobile access issue
# Run this on your VPS after deployment

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}🔧 FateVerse Mobile Access Fix${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if running on VPS (not localhost)
if [ -z "$VPS_IP" ]; then
    echo -e "${YELLOW}📡 Detecting VPS IP...${NC}"
    VPS_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null)
    
    if [ -z "$VPS_IP" ]; then
        echo -e "${RED}❌ Could not detect VPS IP automatically${NC}"
        echo -e "${YELLOW}Please enter your VPS IP address:${NC}"
        read -p "VPS IP: " VPS_IP
    fi
fi

echo -e "${GREEN}✓ VPS IP: $VPS_IP${NC}"
echo ""

# Check if Google Client ID is set
if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo -e "${YELLOW}Please enter your Google OAuth Client ID:${NC}"
    read -p "Google Client ID: " GOOGLE_CLIENT_ID
fi

# Generate JWT Secret
JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | base64)

echo -e "${YELLOW}📝 Creating backend/.env file...${NC}"

# Create backend .env
cat > backend/.env << EOF
# MongoDB Configuration
MONGODB_URL=mongodb://fateverse:fateverse123@mongodb:27017/fateverse?authSource=admin

# JWT Configuration
JWT_SECRET=${JWT_SECRET}

# Google OAuth Configuration
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}

# CORS Configuration - Allow frontend origins
CORS_ORIGINS=http://${VPS_IP}:3000,http://${VPS_IP},http://localhost:3000,http://localhost

# Environment
NODE_ENV=production
EOF

echo -e "${GREEN}✓ Created backend/.env${NC}"

echo -e "${YELLOW}📝 Creating frontend/.env file...${NC}"

# Create frontend .env
cat > frontend/.env << EOF
# API Configuration - Point to VPS backend
VITE_API_URL=http://${VPS_IP}:8000

# Google OAuth Configuration
VITE_GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
EOF

echo -e "${GREEN}✓ Created frontend/.env${NC}"
echo ""

# Check and configure firewall
echo -e "${YELLOW}🔥 Configuring firewall...${NC}"

if command -v ufw &> /dev/null; then
    sudo ufw allow 8000/tcp comment 'FateVerse Backend API' 2>/dev/null
    sudo ufw allow 3000/tcp comment 'FateVerse Frontend' 2>/dev/null
    sudo ufw allow 80/tcp comment 'HTTP' 2>/dev/null
    sudo ufw allow 443/tcp comment 'HTTPS' 2>/dev/null
    echo -e "${GREEN}✓ Firewall rules added (UFW)${NC}"
else
    echo -e "${YELLOW}⚠ UFW not found. Please open ports manually:${NC}"
    echo -e "  - Port 8000 (Backend API)"
    echo -e "  - Port 3000 (Frontend)"
    echo -e "  - Port 80 (HTTP)"
    echo -e "  - Port 443 (HTTPS)"
fi

echo ""

# Restart containers
echo -e "${YELLOW}🐳 Restarting Docker containers...${NC}"

if command -v docker &> /dev/null; then
    docker compose down 2>/dev/null
    docker compose up -d --build
    
    echo -e "${GREEN}✓ Containers restarted${NC}"
    echo ""
    
    # Wait for containers to be healthy
    echo -e "${YELLOW}⏳ Waiting for services to be healthy...${NC}"
    sleep 10
    
    # Check container status
    echo -e "${YELLOW}📊 Container Status:${NC}"
    docker compose ps
else
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}📱 Mobile Access URLs:${NC}"
echo -e "  Frontend: ${GREEN}http://${VPS_IP}:3000${NC}"
echo -e "  Backend:  ${GREEN}http://${VPS_IP}:8000${NC}"
echo ""
echo -e "${YELLOW}🧪 Test Commands:${NC}"
echo -e "  Health Check: curl http://${VPS_IP}:8000/health"
echo -e "  View Logs:    docker compose logs -f"
echo ""
echo -e "${YELLOW}⚠ Important Notes:${NC}"
echo -e "  1. Make sure your cloud firewall (AWS/DO/GCP) allows ports 3000 and 8000"
echo -e "  2. Test on mobile by accessing: http://${VPS_IP}:3000"
echo -e "  3. For production, consider setting up Nginx reverse proxy"
echo -e "  4. For HTTPS, get SSL certificate using certbot"
echo ""
echo -e "${YELLOW}📖 Documentation:${NC}"
echo -e "  See docs/Mobile_Access_Fix.md for detailed troubleshooting"
echo ""
