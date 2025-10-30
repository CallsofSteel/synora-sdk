# Synora Python SDK

Official Python SDK for Synora X402 Payment Gateway.

## Installation

```bash
pip install synora-sdk
```

## Quick Start

```python
import asyncio
from synora import SynoraClient

async def main():
    client = SynoraClient(
        wallet_private_key="your_private_key",
        api_url="https://api.synora.io"
    )
    
    # Text analysis
    result = await client.call('/tools/analyze', {
        'text': 'What is the sentiment of this text?',
        'model': 'gpt-4'
    })
    print(result)
    
    # OCR
    ocr_result = await client.call('/tools/ocr', {
        'image_url': 'https://example.com/image.png'
    })
    print(ocr_result)

if __name__ == '__main__':
    asyncio.run(main())
```

## Features

- ✅ Async/await support
- ✅ Automatic retry with exponential backoff
- ✅ Type hints
- ✅ Comprehensive error handling
- ✅ Payment caching

## API Reference

### SynoraClient

```python
class SynoraClient:
    def __init__(
        self,
        wallet_private_key: str,
        api_url: str = "https://api.synora.io",
        max_retries: int = 3,
        timeout: int = 30
    )
```

### Methods

#### call(endpoint: str, data: dict) -> dict

Make an API call with automatic payment handling.

```python
result = await client.call('/tools/analyze', {
    'text': 'Hello world',
    'model': 'gpt-4'
})
```

#### get_balance() -> float

Get current USDC balance.

```python
balance = await client.get_balance()
print(f"Balance: ${balance}")
```

## Examples

See [examples](../../examples/python/) directory.

## Requirements

- Python 3.7+
- aiohttp
- web3
- eth-account