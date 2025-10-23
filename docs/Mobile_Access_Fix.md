# Fix Mobile Access Issue - Không Đăng Nhập/Đăng Ký Được Trên Mobile

## 🐛 Vấn đề

**Triệu chứng:**
- Trên laptop/desktop: Đăng nhập/đăng ký OK ✅
- Trên mobile: Không đăng nhập/đăng ký được ❌

**Nguyên nhân:**
1. Frontend đang gọi API `http://localhost:8000` - mobile không thể truy cập localhost của server
2. CORS chưa được cấu hình đúng cho domain production
3. API URL không được set qua environment variable

## ✅ Giải pháp

### 1. Cấu hình Environment Variables trên VPS

#### Backend (.env)
```bash
# Tạo file .env trong folder backend/
cd /path/to/fateverse/backend
nano .env
```

Nội dung:
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://fateverse:fateverse123@mongodb:27017/fateverse?authSource=admin

# JWT Configuration - ĐỔI KEY NÀY!
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-abc123xyz

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-actual-google-client-id.apps.googleusercontent.com

# CORS Configuration - QUAN TRỌNG!
CORS_ORIGINS=http://your-vps-ip,http://your-domain.com,https://your-domain.com

# Environment
NODE_ENV=production
```

**Thay thế:**
- `your-vps-ip`: IP của VPS (ví dụ: `203.0.113.45`)
- `your-domain.com`: Domain của bạn (nếu có)

#### Frontend (.env)
```bash
# Tạo file .env trong folder frontend/
cd /path/to/fateverse/frontend
nano .env
```

Nội dung:
```bash
# API Configuration - QUAN TRỌNG NHẤT!
VITE_API_URL=http://your-vps-ip:8000

# Hoặc nếu có domain:
# VITE_API_URL=https://api.your-domain.com

# Google OAuth Configuration
VITE_GOOGLE_CLIENT_ID=your-actual-google-client-id.apps.googleusercontent.com
```

**Thay thế:**
- `your-vps-ip:8000`: IP VPS + port backend (ví dụ: `http://203.0.113.45:8000`)
- Hoặc dùng domain nếu đã setup reverse proxy

### 2. Cập nhật CORS trong Backend

Sửa file `backend/main.py`:

```python
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, numerology, zodiac, love, tarot, fortune, users, history
from app.database.mongodb import init_db
from datetime import datetime
import uvicorn

app = FastAPI(
    title="FateVerse API - Ứng Dụng Xem Bói",
    description="API Backend cho ứng dụng xem bói FateVerse - Khám phá vận mệnh của bạn",
    version="1.0.0"
)

# Get CORS origins from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost").split(",")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ... rest of the code
```

### 3. Rebuild và Restart Containers

```bash
# Trên VPS, trong folder project
cd /path/to/fateverse

# Rebuild với environment variables mới
docker compose down
docker compose up -d --build

# Kiểm tra logs
docker compose logs -f backend
docker compose logs -f frontend
```

### 4. Mở Port trên Firewall

```bash
# Mở port cho backend API
sudo ufw allow 8000/tcp

# Mở port cho frontend
sudo ufw allow 3000/tcp

# Hoặc port 80/443 nếu dùng Nginx
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Kiểm tra
sudo ufw status
```

### 5. Kiểm tra trên Mobile

1. **Mở browser trên mobile**
2. **Truy cập**: `http://YOUR_VPS_IP:3000`
3. **Thử đăng ký/đăng nhập**
4. **Mở DevTools (nếu có)** hoặc check Network tab

### 6. Debug nếu vẫn lỗi

#### Kiểm tra API có accessible từ mobile không:
```bash
# Trên mobile browser, truy cập:
http://YOUR_VPS_IP:8000/health

# Kết quả mong đợi:
{
  "status": "healthy",
  "timestamp": "2025-10-23T...",
  "service": "FateVerse API"
}
```

#### Kiểm tra logs backend:
```bash
docker compose logs backend --tail=50
```

Tìm dòng có `CORS` hoặc `401`, `403`, `500`

#### Kiểm tra frontend có gọi đúng URL không:
1. Mở DevTools trên mobile (Chrome Remote Debugging)
2. Tab Network
3. Filter: `api`
4. Xem request URL có đúng là `http://YOUR_VPS_IP:8000/api/...` không

## 🎯 Cấu hình Production Hoàn chỉnh (Khuyến nghị)

### Option 1: Dùng Nginx Reverse Proxy (Tốt nhất)

**docker-compose.yml** thêm service nginx:
```yaml
services:
  # ... existing services ...
  
  nginx:
    image: nginx:alpine
    container_name: fateverse-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro  # Nếu có SSL
    depends_on:
      - frontend
      - backend
    networks:
      - fateverse-network
```

**nginx.conf**:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Với cấu hình này:
- **Frontend**: `http://your-domain.com` hoặc `http://your-vps-ip`
- **Backend API**: `http://your-domain.com/api` hoặc `http://your-vps-ip/api`
- **Frontend .env**: `VITE_API_URL=http://your-domain.com` (không cần port 8000!)

### Option 2: Dùng Subdomain

- Frontend: `https://app.your-domain.com`
- Backend API: `https://api.your-domain.com`

## 📝 Checklist

- [ ] Tạo file `.env` cho backend với `CORS_ORIGINS` đúng
- [ ] Tạo file `.env` cho frontend với `VITE_API_URL` đúng (dùng VPS IP hoặc domain)
- [ ] Cập nhật `backend/main.py` để đọc `CORS_ORIGINS` từ environment
- [ ] Rebuild containers: `docker compose up -d --build`
- [ ] Mở port firewall: `sudo ufw allow 8000/tcp && sudo ufw allow 3000/tcp`
- [ ] Test trên mobile: Truy cập `http://VPS_IP:3000`
- [ ] Test API health: `http://VPS_IP:8000/health`
- [ ] Thử đăng ký/đăng nhập trên mobile
- [ ] (Optional) Setup Nginx reverse proxy
- [ ] (Optional) Setup SSL certificate với Let's Encrypt

## 🔍 Common Errors

### Error 1: "Network Error" trên mobile
**Nguyên nhân**: Frontend vẫn gọi `localhost:8000`
**Fix**: Kiểm tra `VITE_API_URL` trong `.env` frontend, phải là IP VPS hoặc domain

### Error 2: CORS error trong console
**Nguyên nhân**: Backend không cho phép origin của frontend
**Fix**: Thêm domain/IP frontend vào `CORS_ORIGINS` trong backend `.env`

### Error 3: "502 Bad Gateway" hoặc "Connection Refused"
**Nguyên nhân**: Backend container chưa chạy hoặc port bị chặn
**Fix**: 
- Check: `docker compose ps`
- Check logs: `docker compose logs backend`
- Mở firewall: `sudo ufw allow 8000/tcp`

### Error 4: "Timeout" khi gọi API
**Nguyên nhân**: Cloud firewall (AWS Security Group, DigitalOcean Firewall) chặn port
**Fix**: Vào panel cloud provider, mở port 8000, 3000 (hoặc 80, 443)

## 🚀 Quick Fix Script

Tạo file `fix-mobile-access.sh`:
```bash
#!/bin/bash

# Màu sắc
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔧 Fixing Mobile Access Issue...${NC}"

# Lấy IP VPS
VPS_IP=$(curl -s ifconfig.me)
echo -e "${GREEN}✓ VPS IP: $VPS_IP${NC}"

# Tạo backend .env
cat > backend/.env << EOF
MONGODB_URL=mongodb://fateverse:fateverse123@mongodb:27017/fateverse?authSource=admin
JWT_SECRET=$(openssl rand -hex 32)
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
CORS_ORIGINS=http://${VPS_IP}:3000,http://${VPS_IP},http://localhost:3000
NODE_ENV=production
EOF

echo -e "${GREEN}✓ Created backend/.env${NC}"

# Tạo frontend .env
cat > frontend/.env << EOF
VITE_API_URL=http://${VPS_IP}:8000
VITE_GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
EOF

echo -e "${GREEN}✓ Created frontend/.env${NC}"

# Mở firewall ports
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp
echo -e "${GREEN}✓ Opened firewall ports${NC}"

# Rebuild containers
docker compose down
docker compose up -d --build

echo -e "${GREEN}✓ Containers rebuilt${NC}"
echo -e "${YELLOW}📱 Try accessing: http://${VPS_IP}:3000 from your mobile${NC}"
```

Chạy:
```bash
chmod +x fix-mobile-access.sh
export GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
./fix-mobile-access.sh
```

---

**Tóm tắt**: Vấn đề là frontend gọi `localhost:8000` nên mobile không truy cập được. Fix bằng cách set `VITE_API_URL` trong frontend `.env` thành IP VPS thực tế, và cấu hình CORS backend chấp nhận origin đó.
