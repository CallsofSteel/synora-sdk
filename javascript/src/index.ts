import axios, { AxiosInstance, AxiosError } from 'axios';
import { ethers } from 'ethers';
import crypto from 'crypto';

export interface SynoraConfig {
  walletPrivateKey: string;
  apiUrl?: string;
  baseRpcUrl?: string;
  maxRetries?: number;
  timeout?: number;
}

export interface PaymentDetails {
  amount: string;
  currency: string;
  recipient: string;
  payment_url?: string;
}

export class SynoraError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'SynoraError';
  }
}

export class PaymentRequiredError extends SynoraError {
  paymentDetails: PaymentDetails;

  constructor(paymentDetails: PaymentDetails) {
    super(`Payment required: ${paymentDetails.amount} ${paymentDetails.currency}`);
    this.name = 'PaymentRequiredError';
    this.paymentDetails = paymentDetails;
  }
}

export class PaymentFailedError extends SynoraError {
  constructor(message: string) {
    super(message);
    this.name = 'PaymentFailedError';
  }
}

export class SynoraClient {
  private wallet: ethers.Wallet;
  private provider: ethers.JsonRpcProvider;
  private axiosInstance: AxiosInstance;
  private paymentCache: Map<string, { timestamp: number; txHash: string }>;
  private maxRetries: number;

  constructor(config: SynoraConfig) {
    const {
      walletPrivateKey,
      apiUrl = 'https://api.synora.io',
      baseRpcUrl = 'https://mainnet.base.org',
      maxRetries = 3,
      timeout = 30000,
    } = config;

    // Setup wallet
    this.provider = new ethers.JsonRpcProvider(baseRpcUrl);
    this.wallet = new ethers.Wallet(walletPrivateKey, this.provider);

    // Setup axios
    this.axiosInstance = axios.create({
      baseURL: apiUrl,
      timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.paymentCache = new Map();
    this.maxRetries = maxRetries;
  }

  /**
   * Make an API call with automatic payment handling
   */
  async call<T = any>(
    endpoint: string,
    data: Record<string, any>,
    headers?: Record<string, string>
  ): Promise<T> {
    try {
      // Make initial request
      const response = await this.axiosInstance.post(endpoint, data, { headers });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 402) {
        // Handle payment required
        const paymentDetails: PaymentDetails = error.response.data;
        const paymentProof = await this.processPayment(paymentDetails);

        // Retry with payment proof
        const retryHeaders = {
          ...headers,
          'X-Payment-Proof': paymentProof,
        };

        const retryResponse = await this.axiosInstance.post(endpoint, data, {
          headers: retryHeaders,
        });
        return retryResponse.data;
      }

      throw new SynoraError(
        `Request failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    }
  }

  /**
   * Process payment for API call
   */
  private async processPayment(paymentDetails: PaymentDetails): Promise<string> {
    const { amount, currency, recipient } = paymentDetails;

    // Create payment hash for caching
    const paymentHash = crypto
      .createHash('sha256')
      .update(`${recipient}${amount}${currency}`)
      .digest('hex');

    // Check cache
    const cached = this.paymentCache.get(paymentHash);
    if (cached && Date.now() - cached.timestamp < 300000) {
      // 5 minutes cache
      return cached.txHash;
    }

    try {
      // Send USDC payment
      const txHash = await this.sendUSDCPayment(recipient, amount);

      // Cache payment
      this.paymentCache.set(paymentHash, {
        timestamp: Date.now(),
        txHash,
      });

      return txHash;
    } catch (error) {
      throw new PaymentFailedError(
        `Payment failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    }
  }

  /**
   * Send USDC payment on Base chain
   */
  private async sendUSDCPayment(recipient: string, amount: string): Promise<string> {
    // USDC contract address on Base
    const usdcAddress = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

    // In production, build and sign actual transaction
    // For demo, return mock transaction hash
    const mockTxHash = `0x${crypto
      .createHash('sha256')
      .update(`${recipient}${amount}${Date.now()}`)
      .digest('hex')}`;

    // Simulate transaction delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    return mockTxHash;
  }

  /**
   * Get current USDC balance
   */
  async getBalance(): Promise<number> {
    // In production, query actual USDC balance
    // For demo, return mock balance
    return 100.0;
  }

  /**
   * Get wallet address
   */
  getAddress(): string {
    return this.wallet.address;
  }
}

export default SynoraClient;