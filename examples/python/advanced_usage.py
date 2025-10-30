# Example: Advanced Usage with Error Handling

import asyncio
import logging
from synora import SynoraClient, SynoraError, PaymentRequiredError, PaymentFailedError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def advanced_example():
    """Advanced usage with error handling and retry logic"""
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        max_retries=3,
        timeout=30
    )
    
    # Check balance first
    try:
        balance = await client.get_balance()
        logger.info(f"Current balance: ${balance}")
        
        if balance < 0.10:
            logger.warning("Low balance! Please add more USDC")
            return
    except Exception as e:
        logger.error(f"Failed to check balance: {e}")
    
    # Multiple API calls with error handling
    tasks = [
        ('analyze', '/tools/analyze', {'text': 'Hello world', 'model': 'gpt-4'}),
        ('ocr', '/tools/ocr', {'image_url': 'https://example.com/image.png'}),
        ('search', '/tools/search', {'query': 'Synora', 'max_results': 3}),
    ]
    
    for name, endpoint, data in tasks:
        try:
            logger.info(f"Calling {name}...")
            result = await client.call(endpoint, data)
            logger.info(f"{name} success: {result}")
            
        except PaymentRequiredError as e:
            logger.error(f"Payment required for {name}: {e.payment_details}")
            
        except PaymentFailedError as e:
            logger.error(f"Payment failed for {name}: {e}")
            
        except SynoraError as e:
            logger.error(f"Synora error for {name}: {e}")
            
        except Exception as e:
            logger.error(f"Unexpected error for {name}: {e}")
        
        # Small delay between requests
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.run(advanced_example())