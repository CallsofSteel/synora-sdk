# Synora SDK - Examples

Complete examples for using Synora SDK.

## Python Examples

### Basic Usage

```bash
cd python
python basic_usage.py
```

Demonstrates:
- Text analysis
- OCR
- Vision analysis
- Web search
- Balance checking

### Advanced Usage

```bash
python advanced_usage.py
```

Demonstrates:
- Error handling
- Retry logic
- Balance checking before requests
- Multiple concurrent requests

## JavaScript Examples

### Basic Usage

```bash
cd javascript
npx ts-node basic_usage.ts
```

### Advanced Usage

```bash
npx ts-node advanced_usage.ts
```

## Setup

### Prerequisites

1. **Wallet with USDC**
   - Get a wallet (MetaMask, Coinbase Wallet)
   - Add USDC on Base chain
   - Export private key

2. **Environment Variables**
   
   Create `.env` file:
   ```bash
   SYNORA_PRIVATE_KEY=your_private_key_here
   ```

3. **Install Dependencies**
   
   Python:
   ```bash
   pip install synora-sdk
   ```
   
   JavaScript:
   ```bash
   npm install @synora/sdk
   ```

## Testing Without Payment

For testing, start the API server with simulate-payment endpoint:

```bash
cd ../../api
python server.py
```

Then in your code:
```python
client = SynoraClient(
    wallet_private_key="test_key",
    api_url="http://localhost:8080"
)
```

## More Examples

See individual example files for detailed comments and explanations.

## Support

- 📖 [Documentation](https://docs.synora.io)
- 💬 [Discord](https://discord.gg/synora)
- 🐛 [Issues](https://github.com/synora/synora-sdk/issues)