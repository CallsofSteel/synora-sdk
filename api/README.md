# Running Synora API Server

## Development Setup

### Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### Run Server

```bash
python server.py
```

Server will start at `http://localhost:8080`

### Test API

```bash
# Health check
curl http://localhost:8080/health

# Get pricing
curl http://localhost:8080/pricing

# Test with simulated payment
curl -X POST http://localhost:8080/simulate-payment \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "/tools/analyze"}'

# Use payment proof
curl -X POST http://localhost:8080/tools/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: <payment_proof_from_above>" \
  -d '{
    "text": "Synora is amazing!",
    "model": "gpt-4",
    "task": "sentiment"
  }'
```

## Production Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Environment Variables

```bash
PORT=8080
ENV=production
```

### Using Uvicorn

```bash
uvicorn server:app --host 0.0.0.0 --port 8080 --workers 4
```

## API Documentation

See [API.md](./API.md) for complete API documentation.