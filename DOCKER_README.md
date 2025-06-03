# 🐳 Docker Deployment Guide for ANN Stock Prediction App

This guide explains how to run the ANN Stock Prediction App using Docker with proper TensorFlow support.

## 📋 Prerequisites

- **Docker** installed on your system
- **Docker Compose** (usually included with Docker Desktop)
- At least **4GB RAM** available for the container
- **2GB free disk space** for the image

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the application
docker-compose up --build

# Access the app at: http://localhost:8501
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t ann-stock-app .

# Run the container
docker run -p 8501:8501 -v $(pwd)/logs:/app/logs ann-stock-app

# Access the app at: http://localhost:8501
```

## 🛠️ Development Mode

For development with hot reload:

```bash
# Run development service
docker-compose --profile dev up ann-stock-app-dev

# Access the dev app at: http://localhost:8502
```

## 📁 Directory Structure

```
ann-stock-prediction-app/
├── Dockerfile              # Main Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Files to exclude from Docker build
├── requirements.txt        # Python dependencies
├── app.py                  # Main Streamlit application
├── data_prep.py            # Data preprocessing
├── model.py                # Neural network model
├── predict.py              # Prediction logic
├── logger.py               # Logging configuration
├── logs/                   # Log files (mounted volume)
├── data/                   # Data files (optional mount)
└── sample_stock_data.csv   # Sample data for testing
```

## 🔧 Configuration Options

### Environment Variables

You can customize the app behavior using environment variables:

```bash
# Set TensorFlow log level (0=all, 1=info, 2=warnings, 3=errors)
export TF_CPP_MIN_LOG_LEVEL=2

# Disable Python bytecode generation
export PYTHONDONTWRITEBYTECODE=1

# Force unbuffered Python output
export PYTHONUNBUFFERED=1
```

### Port Configuration

To run on a different port:

```bash
# Using Docker Compose
docker-compose up --build -p 8080:8501

# Using Docker directly
docker run -p 8080:8501 ann-stock-app
```

## 📊 Volume Mounts

The Docker setup includes volume mounts for:

1. **Logs**: `./logs:/app/logs` - Persist log files
2. **Data**: `./data:/app/data` - Easy access to data files

## 🐛 Troubleshooting

### Common Issues

**1. TensorFlow Installation Issues**
```bash
# If you see TensorFlow errors, try rebuilding without cache
docker-compose build --no-cache
```

**2. Memory Issues**
```bash
# Increase Docker memory limit to at least 4GB
# Docker Desktop: Settings > Resources > Memory
```

**3. Port Already in Use**
```bash
# Check what's using port 8501
netstat -tulpn | grep 8501

# Kill the process or use a different port
docker-compose up --build -p 8502:8501
```

**4. Permission Issues (Linux/Mac)**
```bash
# Fix log directory permissions
sudo chown -R $USER:$USER logs/
```

### Health Check

The container includes a health check. Check status:

```bash
# View container health
docker ps

# View health check logs
docker inspect ann-stock-prediction | grep Health -A 10
```

## 🔍 Monitoring

### View Logs

```bash
# View application logs
docker-compose logs -f ann-stock-app

# View specific log files
docker exec -it ann-stock-prediction tail -f /app/logs/data_prep.log
```

### Container Stats

```bash
# Monitor resource usage
docker stats ann-stock-prediction
```

## 🚦 Production Deployment

### Using Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  ann-stock-app:
    build: .
    ports:
      - "80:8501"
    volumes:
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
      - TF_CPP_MIN_LOG_LEVEL=2
    restart: always
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Security Considerations

1. **Non-root user**: Container runs as non-root user `app`
2. **Minimal base image**: Uses `python:3.9-slim` for smaller attack surface
3. **No unnecessary packages**: Only installs required dependencies
4. **Health checks**: Monitors application health

## 📈 Performance Optimization

### Multi-stage Build (Optional)

For smaller production images, you can use multi-stage builds:

```dockerfile
# Add to Dockerfile for production optimization
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "app.py"]
```

## 🧪 Testing

Test the Docker setup:

```bash
# Build and test
docker-compose up --build

# Upload sample_stock_data.csv
# Try prediction with: 100.50, 101.25, 99.80, 100.75

# Check logs
docker-compose logs ann-stock-app
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [TensorFlow Docker Guide](https://www.tensorflow.org/install/docker)

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify system requirements
3. Try rebuilding without cache: `docker-compose build --no-cache`
4. Check Docker memory allocation (minimum 4GB recommended)
