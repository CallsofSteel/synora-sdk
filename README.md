# Synora SDK

[![npm version](https://badge.fury.io/js/@synora%2Fsdk.svg)](https://www.npmjs.com/package/@synora/sdk)
[![PyPI version](https://badge.fury.io/py/synora-sdk.svg)](https://pypi.org/project/synora-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/synora-sdk.svg)](https://pypi.org/project/synora-sdk/)
[![npm downloads](https://img.shields.io/npm/dm/@synora/sdk.svg)](https://www.npmjs.com/package/@synora/sdk)

🚀 Official SDKs for Synora X402 Payment Gateway

## Overview

Synora provides a simple way to integrate micro-payments into your AI agents and applications using the x402 Payment Required standard. Pay only $0.01 per API call with automatic payment handling.

## Features

- ✅ **No API Keys Required** - Just HTTP requests
- ✅ **Automatic Payment Handling** - SDK handles x402 flow
- ✅ **Multi-Language Support** - Python, JavaScript/TypeScript
- ✅ **USDC Payments** - On-chain transactions via Base
- ✅ **Simple Integration** - 3 lines of code to get started

## Links

- 🌐 **Website**: [https://synora.fi](https://synora.fi)
- 📖 **Documentation**: [https://synora.fi/docs](https://synora.fi/docs)
- 🎮 **Playground**: [https://synora.fi/playground](https://synora.fi/playground)
- 💻 **GitHub**: [https://github.com/synorafi/synora-sdk](https://github.com/synorafi/synora-sdk)

## Available SDKs

- [Python SDK](./python/) - For Python 3.8+
- [JavaScript/TypeScript SDK](./javascript/) - For Node.js 16+ and browsers

## Quick Start

### Python

```python
from synora import SynoraClient

client = SynoraClient(
    wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    base_url="https://api.synora.fi"
)

result = client.text_analysis(
    text='Analyze this text',
    recipient='0x123...',
    amount='0.01'
)
print(result)
```

### JavaScript/TypeScript

```typescript
import { SynoraClient } from 'synora';

const client = new SynoraClient({
  walletAddress: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
  baseUrl: 'https://api.synora.fi'
});

const result = await client.textAnalysis({
  text: 'Analyze this text',
  recipient: '0x123...',
  amount: '0.01'
});
console.log(result);
console.log(result);
```

### Go

```go
import "github.com/synora/synora-go"

client := synora.NewClient("your_private_key")
result, err := client.Call("/tools/analyze", map[string]interface{}{
    "text": "Analyze this text",
    "model": "gpt-4",
})
```

## How It Works

1. **Make Request** - SDK sends HTTP request to Synora gateway
2. **Receive 402** - If payment needed, gateway returns HTTP 402
3. **Auto Pay** - SDK automatically pays via USDC on Base chain
4. **Retry & Get Result** - SDK retries with payment proof and returns result

## API Endpoints

### Base URL
```
https://api.synora.io
```

### Available Tools

- `POST /tools/analyze` - Text analysis with LLMs
- `POST /tools/ocr` - Optical character recognition
- `POST /tools/vision` - Image analysis
- `POST /tools/search` - Web search
- `POST /tools/translate` - Language translation

## Installation

### Python
```bash
pip install synora-sdk
```

### JavaScript/TypeScript
```bash
npm install @synora/sdk
# or
yarn add @synora/sdk
```

### Go
```bash
go get github.com/synora/synora-go
```

## Configuration

### Wallet Setup

You need a wallet with USDC on Base chain:

1. Create a wallet (MetaMask, Coinbase Wallet, etc.)
2. Get some USDC on Base chain
3. Export your private key
4. Use it in SDK initialization

### Environment Variables

```bash
SYNORA_PRIVATE_KEY=your_private_key
SYNORA_API_URL=https://api.synora.io
```

## Examples

See the `examples/` directory for complete examples:

- [Python Examples](./examples/python/)
- [JavaScript Examples](./examples/javascript/)
- [Go Examples](./examples/go/)

## Pricing

- Text Analysis: $0.01 per request
- OCR: $0.02 per image
- Vision Analysis: $0.03 per image
- Web Search: $0.01 per query
- Translation: $0.01 per text

## Support

- 📖 [Documentation](https://docs.synora.io)
- 💬 [Discord Community](https://discord.gg/synora)
- 🐛 [Issue Tracker](https://github.com/synora/synora-sdk/issues)
- 📧 Email: support@synora.io

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Security

⚠️ Never commit your private keys! Use environment variables.

For security issues, email: security@synora.io