/**
 * Authentication Service - Singleton Pattern
 *
 * Ensures only one instance of the auth service exists.
 */

import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

export class AuthService {
  private static instance: AuthService;
  private readonly jwtSecret: string = process.env.JWT_SECRET || 'default-secret';

  /**
   * Private constructor prevents direct instantiation
   */
  private constructor() {
    console.log('AuthService initialized');
  }

  /**
   * Get singleton instance
   */
  static getInstance(): AuthService {
    if (!this.instance) {
      this.instance = new AuthService();
    }
    return this.instance;
  }

  /**
   * Generate JWT token for user
   */
  generateToken(userId: string, role: string): string {
    return jwt.sign(
      { userId, role },
      this.jwtSecret,
      { expiresIn: '15m' }
    );
  }

  /**
   * Verify JWT token
   */
  verifyToken(token: string): any {
    try {
      return jwt.verify(token, this.jwtSecret);
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  /**
   * Hash password with bcrypt
   */
  async hashPassword(password: string): Promise<string> {
    const saltRounds = 10;
    return bcrypt.hash(password, saltRounds);
  }

  /**
   * Compare password with hash
   */
  async comparePassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
}

// Export singleton instance
export const authService = AuthService.getInstance();
