# Build stage
FROM node:18-slim as build

WORKDIR /app

# Build arguments for environment variables
ARG VITE_API_URL
ARG VITE_GOOGLE_CLIENT_ID

# Set environment variables from build args
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID

# Set npm configuration for better network resilience (don't upgrade npm)
RUN npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set registry https://registry.npmjs.org/

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
RUN npm install --no-audit --prefer-offline && \
    npm cache clean --force

# Copy source code
COPY . .

# Build the application with increased memory limit
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN npm run build

# Production stage
FROM nginx:alpine

# Set proper permissions for nginx
RUN mkdir -p /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp /var/cache/nginx/fastcgi_temp /var/cache/nginx/uwsgi_temp /var/cache/nginx/scgi_temp && \
    chown -R nginx:nginx /var/cache/nginx && \
    chmod -R 755 /var/cache/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Security headers
RUN echo "server_tokens off;" > /etc/nginx/conf.d/security.conf \
    && echo "add_header X-Frame-Options SAMEORIGIN;" >> /etc/nginx/conf.d/security.conf \
    && echo "add_header X-Content-Type-Options nosniff;" >> /etc/nginx/conf.d/security.conf \
    && echo "add_header X-XSS-Protection \"1; mode=block\";" >> /etc/nginx/conf.d/security.conf

# Use non-root user
USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]