# Quick Start Guide

## 1. Install SDK

### Python
```bash
pip install synora-sdk
```

### JavaScript
```bash
npm install @synora/sdk
```

## 2. Get Wallet with USDC

1. Create wallet (MetaMask, Coinbase Wallet)
2. Get USDC on Base chain
3. Export private key

⚠️ **Security:** Never commit your private key!

## 3. Use SDK

### Python Example

```python
import asyncio
from synora import SynoraClient

async def main():
    client = SynoraClient(
        wallet_private_key="YOUR_PRIVATE_KEY"
    )
    
    result = await client.call('/tools/analyze', {
        'text': 'Synora is amazing!',
        'model': 'gpt-4'
    })
    
    print(result)

asyncio.run(main())
```

### JavaScript Example

```javascript
import { SynoraClient } from '@synora/sdk';

const client = new SynoraClient({
  walletPrivateKey: 'YOUR_PRIVATE_KEY'
});

const result = await client.call('/tools/analyze', {
  text: 'Synora is amazing!',
  model: 'gpt-4'
});

console.log(result);
```

## 4. Run API Server (Optional)

If you want to run your own instance:

```bash
cd api
pip install -r requirements.txt
python server.py
```

Server runs at `http://localhost:8080`

## Testing

### Test API Without Payment

```bash
# Get payment proof
curl -X POST http://localhost:8080/simulate-payment \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "/tools/analyze"}'

# Use it
curl -X POST http://localhost:8080/tools/analyze \
  -H "X-Payment-Proof: <proof_from_above>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "model": "gpt-4"}'
```

## Next Steps

- Read [API Documentation](./api/API.md)
- See [Examples](./examples/)
- Join [Discord Community](https://discord.gg/synora)
- Star on [GitHub](https://github.com/synora/synora-sdk)

## Support

- 📚 [Documentation](https://docs.synora.io)
- 💬 [Discord](https://discord.gg/synora)
- 📧 Email: support@synora.io