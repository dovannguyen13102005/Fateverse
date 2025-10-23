# FateVerse - VPS Deployment Guide

Complete guide to deploy FateVerse application to a VPS using Docker and Docker Compose.

## Prerequisites

### VPS Requirements
- Ubuntu 20.04 LTS or newer (or any Linux distribution)
- Minimum 2GB RAM (4GB recommended)
- 20GB disk space
- Public IP address
- Domain name (optional but recommended)

### Local Requirements
- Git
- SSH access to your VPS
- Domain DNS configured (if using custom domain)

## Step 1: Initial VPS Setup

### 1.1 Connect to VPS
```bash
ssh root@your-vps-ip
# or
ssh your-username@your-vps-ip
```

### 1.2 Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.3 Create Non-Root User (if not exists)
```bash
# Create user
sudo adduser fateverse

# Add to sudo group
sudo usermod -aG sudo fateverse

# Switch to new user
su - fateverse
```

### 1.4 Setup Firewall
```bash
# Allow SSH
sudo ufw allow OpenSSH

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## Step 2: Install Docker

### 2.1 Install Docker Engine
```bash
# Install dependencies
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Add user to docker group
sudo usermod -aG docker ${USER}

# Apply group changes (or logout and login again)
newgrp docker

# Verify installation
docker --version
```

### 2.2 Install Docker Compose
```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

## Step 3: Clone Repository

### 3.1 Install Git (if not installed)
```bash
sudo apt install git -y
```

### 3.2 Clone FateVerse Repository
```bash
# Navigate to home directory
cd ~

# Clone repository
git clone https://github.com/dovannguyen13102005/Fateverse.git

# Navigate to project directory
cd Fateverse
```

## Step 4: Configure Environment Variables

### 4.1 Create Backend .env File
```bash
cd ~/Fateverse/backend
nano .env
```

Add the following content (replace with your actual values):
```env
# MongoDB Configuration
MONGODB_URI=mongodb://mongodb:27017
MONGODB_DB_NAME=fateverse

# JWT Secret (generate a strong random string)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS (add your domain)
CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

**To generate a secure JWT secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.2 Create Frontend .env File
```bash
cd ~/Fateverse/frontend
nano .env
```

Add the following content:
```env
# API Configuration
VITE_API_URL=http://your-vps-ip:8000/api
# or with domain:
# VITE_API_URL=https://api.yourdomain.com/api

# Google OAuth Client ID
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

## Step 5: Configure Google OAuth

### 5.1 Get Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Add Authorized JavaScript origins:
   - `http://your-vps-ip:3000`
   - `https://yourdomain.com` (if using domain)
6. Add Authorized redirect URIs:
   - `http://your-vps-ip:3000`
   - `https://yourdomain.com` (if using domain)

## Step 6: Update Docker Compose for Production

### 6.1 Edit docker-compose.yml
```bash
cd ~/Fateverse
nano docker-compose.yml
```

Modify the file to use environment variables:
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: fateverse-mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=fateverse
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fateverse-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      mongodb:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: fateverse-frontend
    restart: unless-stopped
    ports:
      - "3000:80"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mongodb_data:
```

## Step 7: Deploy Application

### 7.1 Build and Start Containers
```bash
cd ~/Fateverse

# Build images
docker-compose build

# Start services in detached mode
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 7.2 Verify Deployment
```bash
# Check if all containers are running
docker-compose ps

# Test backend API
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

## Step 8: Setup Nginx Reverse Proxy (Optional but Recommended)

### 8.1 Install Nginx
```bash
sudo apt install nginx -y
```

### 8.2 Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/fateverse
```

Add the following configuration:
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 8.3 Enable Site
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/fateverse /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx on boot
sudo systemctl enable nginx
```

## Step 9: Setup SSL with Let's Encrypt (Optional but Recommended)

### 9.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 9.2 Obtain SSL Certificate
```bash
# For frontend domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For backend API domain
sudo certbot --nginx -d api.yourdomain.com
```

### 9.3 Auto-Renewal Setup
```bash
# Test renewal
sudo certbot renew --dry-run

# Certificate will auto-renew via cron
```

## Step 10: Update Frontend Environment for Production

After setting up SSL and domain, update frontend .env:
```bash
cd ~/Fateverse/frontend
nano .env
```

Update to use HTTPS:
```env
VITE_API_URL=https://api.yourdomain.com/api
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

Rebuild frontend:
```bash
cd ~/Fateverse
docker-compose up -d --build frontend
```

## Step 11: Database Backup Setup

### 11.1 Create Backup Script
```bash
mkdir -p ~/backups
nano ~/backups/backup-mongodb.sh
```

Add the following content:
```bash
#!/bin/bash
BACKUP_DIR=~/backups/mongodb
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="fateverse_backup_$TIMESTAMP"

# Create backup directory
mkdir -p $BACKUP_DIR

# Run backup
docker exec fateverse-mongodb mongodump --out /tmp/$BACKUP_NAME --db fateverse

# Copy backup from container
docker cp fateverse-mongodb:/tmp/$BACKUP_NAME $BACKUP_DIR/

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR/$BACKUP_NAME"
```

Make executable:
```bash
chmod +x ~/backups/backup-mongodb.sh
```

### 11.2 Setup Cron Job for Auto Backup
```bash
crontab -e
```

Add daily backup at 2 AM:
```cron
0 2 * * * /home/fateverse/backups/backup-mongodb.sh >> /home/fateverse/backups/backup.log 2>&1
```

## Step 12: Maintenance Commands

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### View Logs
```bash
# All logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Update Application
```bash
cd ~/Fateverse

# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Clean Up Docker
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused containers
docker container prune
```

## Step 13: Monitoring Setup (Optional)

### 13.1 Install htop for System Monitoring
```bash
sudo apt install htop -y
htop
```

### 13.2 Monitor Docker Resources
```bash
# Resource usage
docker stats

# Disk usage
docker system df
```

## Security Best Practices

1. **Change Default Ports** (optional):
   - Modify `docker-compose.yml` to use different external ports
   - Update firewall rules accordingly

2. **MongoDB Security**:
   - Add authentication to MongoDB
   - Don't expose MongoDB port externally (remove `27017:27017` mapping)

3. **Regular Updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. **Backup Encryption**:
   - Encrypt backups before storing
   - Store backups off-site

5. **Use Strong Passwords**:
   - JWT_SECRET_KEY: 32+ characters random string
   - Database passwords: Strong and unique

6. **Monitor Logs**:
   ```bash
   # Check for suspicious activity
   docker-compose logs backend | grep -i error
   ```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs service-name

# Check if port is in use
sudo netstat -tulpn | grep PORT_NUMBER

# Remove and rebuild
docker-compose down -v
docker-compose up -d --build
```

### Database Connection Issues
```bash
# Check MongoDB is running
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Test connection from backend
docker exec -it fateverse-backend ping mongodb
```

### Frontend Can't Connect to Backend
```bash
# Check CORS settings in backend/.env
# Verify VITE_API_URL in frontend/.env
# Check if backend is accessible
curl http://localhost:8000/health
```

### SSL Certificate Issues
```bash
# Renew certificates
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

## Performance Optimization

### 1. Enable Docker Compose Production Mode
Add to `docker-compose.yml`:
```yaml
services:
  backend:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          memory: 512M
```

### 2. Enable Nginx Caching
Add to Nginx config:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
proxy_cache my_cache;
```

### 3. MongoDB Optimization
```bash
# Increase MongoDB memory
# Edit docker-compose.yml mongodb service:
environment:
  - MONGO_INITDB_DATABASE=fateverse
command: mongod --wiredTigerCacheSizeGB 1.5
```

## Support and Resources

- **Repository**: https://github.com/dovannguyen13102005/Fateverse
- **Docker Docs**: https://docs.docker.com/
- **Nginx Docs**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/

## Quick Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Update application
git pull && docker-compose up -d --build

# Backup database
docker exec fateverse-mongodb mongodump --out /tmp/backup --db fateverse

# Restart service
docker-compose restart backend

# Check status
docker-compose ps

# Access container shell
docker exec -it fateverse-backend bash
```

---

**Congratulations!** 🎉 Your FateVerse application is now deployed on VPS with Docker!

For support, please open an issue on GitHub: https://github.com/dovannguyen13102005/Fateverse/issues
