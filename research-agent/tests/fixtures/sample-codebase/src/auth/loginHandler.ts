/**
 * Login Handler - Authentication Flow
 *
 * Handles user login with JWT token generation.
 */

import { Request, Response } from 'express';
import { authService } from '../services/authService';
import { UserRepository } from './userRepository';

export interface LoginRequest {
  email: string;
  password: string;
}

export class LoginHandler {
  private userRepo: UserRepository;

  constructor() {
    this.userRepo = new UserRepository();
  }

  /**
   * Handle login request
   *
   * Flow:
   * 1. Validate credentials
   * 2. Find user in database
   * 3. Verify password
   * 4. Generate JWT token
   * 5. Set HTTP-only cookie
   * 6. Return user data
   */
  async handle(req: Request, res: Response): Promise<void> {
    try {
      const { email, password } = req.body as LoginRequest;

      // Step 1: Validate input
      if (!email || !password) {
        res.status(400).json({ error: 'Email and password required' });
        return;
      }

      // Step 2: Find user
      const user = await this.userRepo.findByEmail(email);
      if (!user) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }

      // Step 3: Verify password
      const isValid = await authService.comparePassword(password, user.passwordHash);
      if (!isValid) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }

      // Step 4: Generate token
      const token = authService.generateToken(user.id, user.role);

      // Step 5: Set cookie
      res.cookie('access-token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 15 * 60 * 1000 // 15 minutes
      });

      // Step 6: Return user data (without sensitive info)
      res.json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        }
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
