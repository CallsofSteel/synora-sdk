import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from eth_account import Account
from web3 import Web3
import time
import hashlib


class SynoraError(Exception):
    """Base exception for Synora SDK"""
    pass


class PaymentRequiredError(SynoraError):
    """Raised when HTTP 402 Payment Required is received"""
    def __init__(self, payment_details: Dict[str, Any]):
        self.payment_details = payment_details
        super().__init__(f"Payment required: {payment_details.get('amount')} {payment_details.get('currency')}")


class PaymentFailedError(SynoraError):
    """Raised when payment transaction fails"""
    pass


class SynoraClient:
    """
    Synora SDK Client for Python
    
    Handles automatic x402 payment flow for API calls.
    
    Example:
        >>> client = SynoraClient(wallet_private_key="0x...")
        >>> result = await client.call('/tools/analyze', {'text': 'Hello'})
    """
    
    def __init__(
        self,
        wallet_private_key: str,
        api_url: str = "https://api.synora.io",
        base_rpc_url: str = "https://mainnet.base.org",
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize Synora client.
        
        Args:
            wallet_private_key: Ethereum private key for payments
            api_url: Synora API base URL
            base_rpc_url: Base chain RPC URL
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Setup wallet
        self.account = Account.from_key(wallet_private_key)
        self.web3 = Web3(Web3.HTTPProvider(base_rpc_url))
        
        # Payment cache to avoid duplicate payments
        self._payment_cache = {}
        
    async def call(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make an API call with automatic payment handling.
        
        Args:
            endpoint: API endpoint (e.g., '/tools/analyze')
            data: Request payload
            headers: Optional HTTP headers
            
        Returns:
            API response as dictionary
            
        Raises:
            SynoraError: If request fails
            PaymentFailedError: If payment fails
        """
        url = f"{self.api_url}{endpoint}"
        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        
        async with aiohttp.ClientSession() as session:
            # Make initial request
            async with session.post(
                url,
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                
                # If successful, return result
                if response.status == 200:
                    return await response.json()
                
                # Handle payment required
                if response.status == 402:
                    payment_details = await response.json()
                    
                    # Process payment
                    payment_proof = await self._process_payment(payment_details)
                    
                    # Retry with payment proof
                    headers['X-Payment-Proof'] = payment_proof
                    
                    async with session.post(
                        url,
                        json=data,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as retry_response:
                        if retry_response.status == 200:
                            return await retry_response.json()
                        else:
                            error_text = await retry_response.text()
                            raise SynoraError(f"Request failed after payment: {error_text}")
                
                # Handle other errors
                error_text = await response.text()
                raise SynoraError(f"Request failed with status {response.status}: {error_text}")
    
    async def _process_payment(self, payment_details: Dict[str, Any]) -> str:
        """
        Process payment for API call.
        
        Args:
            payment_details: Payment information from 402 response
            
        Returns:
            Payment proof (transaction hash)
        """
        amount = payment_details.get('amount')
        currency = payment_details.get('currency', 'USDC')
        recipient = payment_details.get('recipient')
        payment_url = payment_details.get('payment_url')
        
        # Create payment hash for caching
        payment_hash = hashlib.sha256(
            f"{recipient}{amount}{currency}".encode()
        ).hexdigest()
        
        # Check cache
        if payment_hash in self._payment_cache:
            cached_time, tx_hash = self._payment_cache[payment_hash]
            if time.time() - cached_time < 300:  # 5 minutes cache
                return tx_hash
        
        try:
            # In production, this would call the actual payment facilitator
            # For now, we simulate the payment
            tx_hash = await self._send_usdc_payment(recipient, amount)
            
            # Cache payment
            self._payment_cache[payment_hash] = (time.time(), tx_hash)
            
            return tx_hash
            
        except Exception as e:
            raise PaymentFailedError(f"Payment failed: {str(e)}")
    
    async def _send_usdc_payment(self, recipient: str, amount: str) -> str:
        """
        Send USDC payment on Base chain.
        
        Args:
            recipient: Recipient address
            amount: Amount in USDC
            
        Returns:
            Transaction hash
        """
        # USDC contract address on Base
        usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        
        # In production, build and sign actual transaction
        # For demo, return mock transaction hash
        mock_tx_hash = f"0x{hashlib.sha256(f'{recipient}{amount}{time.time()}'.encode()).hexdigest()}"
        
        # Simulate transaction delay
        await asyncio.sleep(1)
        
        return mock_tx_hash
    
    async def get_balance(self) -> float:
        """
        Get current USDC balance.
        
        Returns:
            Balance in USDC
        """
        # In production, query actual USDC balance
        # For demo, return mock balance
        return 100.0
    
    def get_address(self) -> str:
        """
        Get wallet address.
        
        Returns:
            Ethereum address
        """
        return self.account.address


__all__ = ['SynoraClient', 'SynoraError', 'PaymentRequiredError', 'PaymentFailedError']