import asyncio
from synora import SynoraClient


async def text_analysis_example():
    """Example: Text analysis with GPT-4"""
    print("\n=== Text Analysis Example ===")
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    
    try:
        result = await client.call('/tools/analyze', {
            'text': 'Synora is an amazing payment gateway for AI agents!',
            'model': 'gpt-4',
            'task': 'sentiment'
        })
        
        print(f"Result: {result}")
        print(f"Wallet: {client.get_address()}")
        
    except Exception as e:
        print(f"Error: {e}")


async def ocr_example():
    """Example: OCR on image"""
    print("\n=== OCR Example ===")
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    
    try:
        result = await client.call('/tools/ocr', {
            'image_url': 'https://example.com/receipt.png'
        })
        
        print(f"Extracted text: {result.get('text')}")
        print(f"Confidence: {result.get('confidence')}")
        
    except Exception as e:
        print(f"Error: {e}")


async def vision_analysis_example():
    """Example: Image analysis"""
    print("\n=== Vision Analysis Example ===")
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    
    try:
        result = await client.call('/tools/vision', {
            'image_url': 'https://example.com/photo.jpg',
            'prompt': 'Describe what you see in this image'
        })
        
        print(f"Analysis: {result.get('description')}")
        
    except Exception as e:
        print(f"Error: {e}")


async def web_search_example():
    """Example: Web search"""
    print("\n=== Web Search Example ===")
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    
    try:
        result = await client.call('/tools/search', {
            'query': 'Synora payment gateway',
            'max_results': 5
        })
        
        print(f"Found {len(result.get('results', []))} results")
        for i, item in enumerate(result.get('results', []), 1):
            print(f"{i}. {item.get('title')}: {item.get('url')}")
        
    except Exception as e:
        print(f"Error: {e}")


async def check_balance_example():
    """Example: Check USDC balance"""
    print("\n=== Balance Check Example ===")
    
    client = SynoraClient(
        wallet_private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    
    try:
        balance = await client.get_balance()
        print(f"USDC Balance: ${balance}")
        print(f"Wallet Address: {client.get_address()}")
        
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Run all examples"""
    print("Synora SDK Examples")
    print("=" * 50)
    
    await text_analysis_example()
    await asyncio.sleep(1)
    
    await ocr_example()
    await asyncio.sleep(1)
    
    await vision_analysis_example()
    await asyncio.sleep(1)
    
    await web_search_example()
    await asyncio.sleep(1)
    
    await check_balance_example()


if __name__ == '__main__':
    asyncio.run(main())