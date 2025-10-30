# Testing Guide

## Local Testing Setup

### 1. Start API Server

```bash
cd api
pip install -r requirements.txt
python server.py
```

Server will run at `http://localhost:8080`

### 2. Test Endpoints

#### Health Check
```bash
curl http://localhost:8080/health
```

#### Get Pricing
```bash
curl http://localhost:8080/pricing
```

#### Test 402 Flow
```bash
# This will return 402 Payment Required
curl -X POST http://localhost:8080/tools/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "model": "gpt-4"}'
```

### 3. Simulate Payment

```bash
# Get payment proof
curl -X POST http://localhost:8080/simulate-payment \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "/tools/analyze"}'

# Response will include payment_proof
# {
#   "payment_proof": "abc123...",
#   "endpoint": "/tools/analyze",
#   "amount": 0.01
# }
```

### 4. Use Payment Proof

```bash
curl -X POST http://localhost:8080/tools/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: <payment_proof_from_above>" \
  -d '{
    "text": "Synora is amazing!",
    "model": "gpt-4",
    "task": "sentiment"
  }'
```

## SDK Testing

### Python SDK

```bash
cd python

# Install in development mode
pip install -e .

# Run examples
cd ../examples/python
python basic_usage.py
python advanced_usage.py
```

### JavaScript SDK

```bash
cd javascript

# Install dependencies
npm install

# Build
npm run build

# Run examples
cd ../examples/javascript
npx ts-node basic_usage.ts
npx ts-node advanced_usage.ts
```

## Integration Testing

### Test All Endpoints

```python
import asyncio
from synora import SynoraClient

async def test_all_endpoints():
    client = SynoraClient(
        wallet_private_key="test_key",
        api_url="http://localhost:8080"
    )
    
    # Get payment proof first
    # (In real usage, SDK handles this automatically)
    
    endpoints = [
        ('/tools/analyze', {'text': 'Test', 'model': 'gpt-4'}),
        ('/tools/ocr', {'image_url': 'https://example.com/img.png'}),
        ('/tools/vision', {'image_url': 'https://example.com/img.png', 'prompt': 'Describe'}),
        ('/tools/search', {'query': 'Synora', 'max_results': 5}),
        ('/tools/translate', {'text': 'Hello', 'target_language': 'es'}),
    ]
    
    for endpoint, data in endpoints:
        try:
            result = await client.call(endpoint, data)
            print(f"✓ {endpoint}: Success")
        except Exception as e:
            print(f"✗ {endpoint}: {e}")

asyncio.run(test_all_endpoints())
```

## Performance Testing

### Load Test with Apache Bench

```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Ubuntu/Debian
brew install httpie  # macOS

# Test endpoint
ab -n 1000 -c 10 -p data.json -T application/json \
  -H "X-Payment-Proof: your_proof" \
  http://localhost:8080/tools/analyze
```

### Load Test with Python

```python
import asyncio
import time
from synora import SynoraClient

async def load_test():
    client = SynoraClient(
        wallet_private_key="test_key",
        api_url="http://localhost:8080"
    )
    
    start = time.time()
    tasks = []
    
    # 100 concurrent requests
    for i in range(100):
        task = client.call('/tools/analyze', {
            'text': f'Test {i}',
            'model': 'gpt-4'
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start
    successful = sum(1 for r in results if not isinstance(r, Exception))
    
    print(f"Total: 100 requests")
    print(f"Successful: {successful}")
    print(f"Failed: {100 - successful}")
    print(f"Time: {elapsed:.2f}s")
    print(f"RPS: {100/elapsed:.2f}")

asyncio.run(load_test())
```

## Debugging

### Enable Debug Logging

Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from synora import SynoraClient
client = SynoraClient(...)
```

JavaScript:
```typescript
// Set environment variable
process.env.DEBUG = 'synora:*';

import { SynoraClient } from '@synora/sdk';
```

### Check Payment Cache

Python:
```python
client = SynoraClient(...)
print(client._payment_cache)  # View cached payments
```

JavaScript:
```typescript
const client = new SynoraClient(...);
console.log(client['paymentCache']);  // View cached payments
```

## Common Issues

### Issue: "Payment Required" not resolved

**Solution:** Check if payment proof is correct and not expired (5 min cache)

### Issue: "Connection refused"

**Solution:** Make sure API server is running on correct port

### Issue: "Invalid payment proof"

**Solution:** Generate new payment proof using `/simulate-payment`

## CI/CD Testing

### GitHub Actions Example

```yaml
name: Test SDK

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd python
        pip install -e .
    
    - name: Start API server
      run: |
        cd api
        python server.py &
        sleep 5
    
    - name: Run tests
      run: |
        cd examples/python
        python basic_usage.py
```

## Support

For testing issues:
- \ud83d\udc1b [Report Bug](https://github.com/synora/synora-sdk/issues)
- \ud83d\udcac [Discord](https://discord.gg/synora)
- \ud83d\udce7 Email: support@synora.io
