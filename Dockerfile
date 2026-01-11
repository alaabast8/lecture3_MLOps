# Stage 1: Build React Frontend
FROM node:18-alpine 

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm i 

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Setup Python Backend
FROM python:3.11-slim AS backend-setup

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Stage 3: Final Production Image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend-setup /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-setup /usr/local/bin /usr/local/bin
COPY --from=backend-setup /app/backend /app/backend

# Copy built frontend from frontend-build stage
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Copy nginx configuration


# Create startup script
RUN echo '#!/bin/bash\n\
nginx\n\
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 80 8000

# Set environment variable
ENV ENV=local

# Start both services
CMD ["/app/start.sh"]