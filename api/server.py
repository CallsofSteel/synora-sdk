from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import hashlib
import time
import uuid

app = FastAPI(
    title="Synora API",
    description="X402 Payment Gateway for AI Agents",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
payment_proofs = {}
usage_logs = []

# Pricing (in USDC)
PRICING = {
    "/tools/analyze": 0.01,
    "/tools/ocr": 0.02,
    "/tools/vision": 0.03,
    "/tools/search": 0.01,
    "/tools/translate": 0.01,
}


class AnalyzeRequest(BaseModel):
    text: str
    model: str = "gpt-4"
    task: str = "sentiment"


class OCRRequest(BaseModel):
    image_url: str


class VisionRequest(BaseModel):
    image_url: str
    prompt: str


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "auto"


class PaymentResponse(BaseModel):
    amount: str
    currency: str
    recipient: str
    payment_url: str
    challenge: str


def verify_payment(payment_proof: str, endpoint: str) -> bool:
    """Verify payment proof"""
    if payment_proof in payment_proofs:
        proof_data = payment_proofs[payment_proof]
        # Check if payment is for correct endpoint and not expired
        if proof_data['endpoint'] == endpoint and time.time() - proof_data['timestamp'] < 3600:
            return True
    return False


def require_payment(endpoint: str) -> PaymentResponse:
    """Generate payment requirement"""
    amount = PRICING.get(endpoint, 0.01)
    challenge = str(uuid.uuid4())
    
    return PaymentResponse(
        amount=str(amount),
        currency="USDC",
        recipient="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",  # Example address
        payment_url="https://facilitator.synora.io/pay",
        challenge=challenge
    )


@app.get("/")
async def root():
    return {
        "name": "Synora API",
        "version": "0.1.0",
        "status": "operational",
        "endpoints": list(PRICING.keys())
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}


@app.get("/pricing")
async def get_pricing():
    return {
        "currency": "USDC",
        "prices": PRICING
    }


@app.post("/tools/analyze")
async def analyze_text(
    request: AnalyzeRequest,
    x_payment_proof: Optional[str] = Header(None)
):
    """Text analysis endpoint"""
    endpoint = "/tools/analyze"
    
    # Check payment
    if not x_payment_proof or not verify_payment(x_payment_proof, endpoint):
        raise HTTPException(
            status_code=402,
            detail=require_payment(endpoint).dict()
        )
    
    # Process request
    # In production, call actual LLM API
    result = {
        "text": request.text,
        "model": request.model,
        "task": request.task,
        "sentiment": "positive",
        "confidence": 0.95,
        "analysis": "This text expresses a positive sentiment about Synora.",
        "timestamp": time.time()
    }
    
    # Log usage
    usage_logs.append({
        "endpoint": endpoint,
        "payment_proof": x_payment_proof,
        "timestamp": time.time()
    })
    
    return result


@app.post("/tools/ocr")
async def ocr_image(
    request: OCRRequest,
    x_payment_proof: Optional[str] = Header(None)
):
    """OCR endpoint"""
    endpoint = "/tools/ocr"
    
    # Check payment
    if not x_payment_proof or not verify_payment(x_payment_proof, endpoint):
        raise HTTPException(
            status_code=402,
            detail=require_payment(endpoint).dict()
        )
    
    # Process request
    # In production, call actual OCR API
    result = {
        "image_url": request.image_url,
        "text": "Sample extracted text from image",
        "confidence": 0.98,
        "language": "en",
        "timestamp": time.time()
    }
    
    usage_logs.append({
        "endpoint": endpoint,
        "payment_proof": x_payment_proof,
        "timestamp": time.time()
    })
    
    return result


@app.post("/tools/vision")
async def vision_analysis(
    request: VisionRequest,
    x_payment_proof: Optional[str] = Header(None)
):
    """Vision analysis endpoint"""
    endpoint = "/tools/vision"
    
    # Check payment
    if not x_payment_proof or not verify_payment(x_payment_proof, endpoint):
        raise HTTPException(
            status_code=402,
            detail=require_payment(endpoint).dict()
        )
    
    # Process request
    # In production, call actual vision API
    result = {
        "image_url": request.image_url,
        "prompt": request.prompt,
        "description": "A beautiful landscape with mountains and a lake",
        "objects": ["mountain", "lake", "sky", "trees"],
        "confidence": 0.96,
        "timestamp": time.time()
    }
    
    usage_logs.append({
        "endpoint": endpoint,
        "payment_proof": x_payment_proof,
        "timestamp": time.time()
    })
    
    return result


@app.post("/tools/search")
async def web_search(
    request: SearchRequest,
    x_payment_proof: Optional[str] = Header(None)
):
    """Web search endpoint"""
    endpoint = "/tools/search"
    
    # Check payment
    if not x_payment_proof or not verify_payment(x_payment_proof, endpoint):
        raise HTTPException(
            status_code=402,
            detail=require_payment(endpoint).dict()
        )
    
    # Process request
    # In production, call actual search API
    results = [
        {
            "title": "Synora - X402 Payment Gateway",
            "url": "https://synora.io",
            "snippet": "Official website for Synora payment gateway"
        },
        {
            "title": "Synora SDK Documentation",
            "url": "https://docs.synora.io",
            "snippet": "Complete SDK documentation for developers"
        }
    ]
    
    usage_logs.append({
        "endpoint": endpoint,
        "payment_proof": x_payment_proof,
        "timestamp": time.time()
    })
    
    return {"query": request.query, "results": results[:request.max_results]}


@app.post("/tools/translate")
async def translate_text(
    request: TranslateRequest,
    x_payment_proof: Optional[str] = Header(None)
):
    """Translation endpoint"""
    endpoint = "/tools/translate"
    
    # Check payment
    if not x_payment_proof or not verify_payment(x_payment_proof, endpoint):
        raise HTTPException(
            status_code=402,
            detail=require_payment(endpoint).dict()
        )
    
    # Process request
    # In production, call actual translation API
    result = {
        "original_text": request.text,
        "translated_text": "Translated version of the text",
        "source_language": request.source_language,
        "target_language": request.target_language,
        "confidence": 0.99,
        "timestamp": time.time()
    }
    
    usage_logs.append({
        "endpoint": endpoint,
        "payment_proof": x_payment_proof,
        "timestamp": time.time()
    })
    
    return result


@app.post("/simulate-payment")
async def simulate_payment(endpoint: str):
    """Simulate payment for testing (development only)"""
    # Generate mock payment proof
    proof = hashlib.sha256(f"{endpoint}{time.time()}".encode()).hexdigest()
    
    payment_proofs[proof] = {
        "endpoint": endpoint,
        "timestamp": time.time(),
        "amount": PRICING.get(endpoint, 0.01)
    }
    
    return {
        "payment_proof": proof,
        "endpoint": endpoint,
        "amount": PRICING.get(endpoint, 0.01),
        "message": "Payment simulated successfully"
    }


@app.get("/usage")
async def get_usage():
    """Get usage statistics"""
    return {
        "total_calls": len(usage_logs),
        "recent_calls": usage_logs[-10:] if usage_logs else []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)