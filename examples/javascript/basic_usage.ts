import { SynoraClient } from '@synora/sdk';

async function textAnalysisExample() {
  console.log('\n=== Text Analysis Example ===');
  
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
  });

  try {
    const result = await client.call('/tools/analyze', {
      text: 'Synora is an amazing payment gateway for AI agents!',
      model: 'gpt-4',
      task: 'sentiment'
    });

    console.log('Result:', result);
    console.log('Wallet:', client.getAddress());
  } catch (error) {
    console.error('Error:', error);
  }
}

async function ocrExample() {
  console.log('\n=== OCR Example ===');
  
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
  });

  try {
    const result = await client.call('/tools/ocr', {
      image_url: 'https://example.com/receipt.png'
    });

    console.log('Extracted text:', result.text);
    console.log('Confidence:', result.confidence);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function visionAnalysisExample() {
  console.log('\n=== Vision Analysis Example ===');
  
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
  });

  try {
    const result = await client.call('/tools/vision', {
      image_url: 'https://example.com/photo.jpg',
      prompt: 'Describe what you see in this image'
    });

    console.log('Analysis:', result.description);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function webSearchExample() {
  console.log('\n=== Web Search Example ===');
  
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
  });

  try {
    const result = await client.call('/tools/search', {
      query: 'Synora payment gateway',
      max_results: 5
    });

    console.log(`Found ${result.results.length} results`);
    result.results.forEach((item: any, i: number) => {
      console.log(`${i + 1}. ${item.title}: ${item.url}`);
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

async function checkBalanceExample() {
  console.log('\n=== Balance Check Example ===');
  
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
  });

  try {
    const balance = await client.getBalance();
    console.log(`USDC Balance: $${balance}`);
    console.log(`Wallet Address: ${client.getAddress()}`);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function main() {
  console.log('Synora SDK Examples');
  console.log('='.repeat(50));

  await textAnalysisExample();
  await new Promise(resolve => setTimeout(resolve, 1000));

  await ocrExample();
  await new Promise(resolve => setTimeout(resolve, 1000));

  await visionAnalysisExample();
  await new Promise(resolve => setTimeout(resolve, 1000));

  await webSearchExample();
  await new Promise(resolve => setTimeout(resolve, 1000));

  await checkBalanceExample();
}

main().catch(console.error);