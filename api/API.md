# Synora API Documentation

## Base URL
```
https://api.synora.io
```

## Authentication

Synora uses HTTP 402 Payment Required for authentication. No API keys needed!

### Flow

1. Make request to endpoint
2. Receive 402 with payment details
3. Pay via USDC on Base chain
4. Retry with `X-Payment-Proof` header

## Endpoints

### Health Check

```http
GET /health
```

Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890
}
```

### Get Pricing

```http
GET /pricing
```

Returns current pricing for all endpoints.

**Response:**
```json
{
  "currency": "USDC",
  "prices": {
    "/tools/analyze": 0.01,
    "/tools/ocr": 0.02,
    "/tools/vision": 0.03,
    "/tools/search": 0.01,
    "/tools/translate": 0.01
  }
}
```

### Text Analysis

```http
POST /tools/analyze
```

Analyze text with LLMs.

**Cost:** $0.01 per request

**Request Body:**
```json
{
  "text": "Synora is amazing!",
  "model": "gpt-4",
  "task": "sentiment"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "analysis": "This text expresses positive sentiment."
}
```

### OCR (Optical Character Recognition)

```http
POST /tools/ocr
```

Extract text from images.

**Cost:** $0.02 per request

**Request Body:**
```json
{
  "image_url": "https://example.com/image.png"
}
```

**Response:**
```json
{
  "text": "Extracted text from image",
  "confidence": 0.98,
  "language": "en"
}
```

### Vision Analysis

```http
POST /tools/vision
```

Analyze images with AI vision.

**Cost:** $0.03 per request

**Request Body:**
```json
{
  "image_url": "https://example.com/photo.jpg",
  "prompt": "Describe this image"
}
```

**Response:**
```json
{
  "description": "A beautiful landscape with mountains",
  "objects": ["mountain", "lake", "sky"],
  "confidence": 0.96
}
```

### Web Search

```http
POST /tools/search
```

Search the web.

**Cost:** $0.01 per request

**Request Body:**
```json
{
  "query": "Synora payment gateway",
  "max_results": 5
}
```

**Response:**
```json
{
  "query": "Synora payment gateway",
  "results": [
    {
      "title": "Synora - Official Site",
      "url": "https://synora.io",
      "snippet": "Official website"
    }
  ]
}
```

### Translation

```http
POST /tools/translate
```

Translate text between languages.

**Cost:** $0.01 per request

**Request Body:**
```json
{
  "text": "Hello world",
  "target_language": "es",
  "source_language": "auto"
}
```

**Response:**
```json
{
  "original_text": "Hello world",
  "translated_text": "Hola mundo",
  "source_language": "en",
  "target_language": "es",
  "confidence": 0.99
}
```

## Error Codes

### 402 Payment Required

Payment needed to access the endpoint.

**Response:**
```json
{
  "amount": "0.01",
  "currency": "USDC",
  "recipient": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "payment_url": "https://facilitator.synora.io/pay",
  "challenge": "uuid-here"
}
```

### 400 Bad Request

Invalid request format.

### 500 Internal Server Error

Server error occurred.

## Rate Limits

- No rate limits with valid payments
- Unlimited requests as long as you pay

## SDKs

Use official SDKs for automatic payment handling:

- [Python SDK](../python/)
- [JavaScript SDK](../javascript/)
- [Go SDK](../go/)

## Testing

### Simulate Payment (Dev Only)

```http
POST /simulate-payment
```

Generate mock payment proof for testing.

**Request Body:**
```json
{
  "endpoint": "/tools/analyze"
}
```

**Response:**
```json
{
  "payment_proof": "abc123...",
  "endpoint": "/tools/analyze",
  "amount": 0.01
}
```

Then use the `payment_proof` in `X-Payment-Proof` header.

## Support

- 📖 [Full Documentation](https://docs.synora.io)
- 💬 [Discord](https://discord.gg/synora)
- 📧 Email: support@synora.io