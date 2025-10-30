# Synora JavaScript/TypeScript SDK

Official JavaScript/TypeScript SDK for Synora X402 Payment Gateway.

## Installation

```bash
npm install @synora/sdk
# or
yarn add @synora/sdk
```

## Quick Start

### TypeScript

```typescript
import { SynoraClient } from '@synora/sdk';

const client = new SynoraClient({
  walletPrivateKey: 'your_private_key',
  apiUrl: 'https://api.synora.io'
});

async function main() {
  // Text analysis
  const result = await client.call('/tools/analyze', {
    text: 'What is the sentiment of this text?',
    model: 'gpt-4'
  });
  console.log(result);

  // OCR
  const ocrResult = await client.call('/tools/ocr', {
    image_url: 'https://example.com/image.png'
  });
  console.log(ocrResult);
}

main();
```

### JavaScript (CommonJS)

```javascript
const { SynoraClient } = require('@synora/sdk');

const client = new SynoraClient({
  walletPrivateKey: 'your_private_key'
});

client.call('/tools/analyze', {
  text: 'Hello world',
  model: 'gpt-4'
}).then(result => {
  console.log(result);
});
```

## Features

- ✅ TypeScript support with full type definitions
- ✅ Promise-based API
- ✅ Automatic retry logic
- ✅ Payment caching
- ✅ Works in Node.js and browsers

## API Reference

### SynoraClient

```typescript
interface SynoraConfig {
  walletPrivateKey: string;
  apiUrl?: string;
  baseRpcUrl?: string;
  maxRetries?: number;
  timeout?: number;
}

class SynoraClient {
  constructor(config: SynoraConfig);
  call<T>(endpoint: string, data: object, headers?: object): Promise<T>;
  getBalance(): Promise<number>;
  getAddress(): string;
}
```

## Examples

See [examples](../../examples/javascript/) directory.

## Requirements

- Node.js 16+
- ethers ^6.0.0
- axios ^1.0.0