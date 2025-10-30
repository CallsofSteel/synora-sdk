// Example: Advanced Usage with Error Handling

import { SynoraClient, SynoraError, PaymentRequiredError, PaymentFailedError } from '@synora/sdk';

async function advancedExample() {
  const client = new SynoraClient({
    walletPrivateKey: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
    maxRetries: 3,
    timeout: 30000
  });

  // Check balance first
  try {
    const balance = await client.getBalance();
    console.log(`Current balance: $${balance}`);

    if (balance < 0.10) {
      console.warn('Low balance! Please add more USDC');
      return;
    }
  } catch (error) {
    console.error('Failed to check balance:', error);
  }

  // Multiple API calls with error handling
  const tasks = [
    { name: 'analyze', endpoint: '/tools/analyze', data: { text: 'Hello world', model: 'gpt-4' } },
    { name: 'ocr', endpoint: '/tools/ocr', data: { image_url: 'https://example.com/image.png' } },
    { name: 'search', endpoint: '/tools/search', data: { query: 'Synora', max_results: 3 } }
  ];

  for (const task of tasks) {
    try {
      console.log(`Calling ${task.name}...`);
      const result = await client.call(task.endpoint, task.data);
      console.log(`${task.name} success:`, result);

    } catch (error) {
      if (error instanceof PaymentRequiredError) {
        console.error(`Payment required for ${task.name}:`, error.paymentDetails);
      } else if (error instanceof PaymentFailedError) {
        console.error(`Payment failed for ${task.name}:`, error.message);
      } else if (error instanceof SynoraError) {
        console.error(`Synora error for ${task.name}:`, error.message);
      } else {
        console.error(`Unexpected error for ${task.name}:`, error);
      }
    }

    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}

advancedExample().catch(console.error);