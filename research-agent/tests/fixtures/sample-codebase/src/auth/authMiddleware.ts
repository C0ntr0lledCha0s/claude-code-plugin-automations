/**
 * Authentication Middleware
 *
 * Protects routes by validating JWT tokens.
 */

import { Request, Response, NextFunction } from 'express';
import { authService } from '../services/authService';
import { UserRepository } from './userRepository';

// Extend Express Request to include user
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        role: string;
      };
    }
  }
}

export class AuthMiddleware {
  private userRepo: UserRepository;

  constructor() {
    this.userRepo = new UserRepository();
  }

  /**
   * Middleware to validate authentication
   *
   * Flow:
   * 1. Extract token from cookie
   * 2. Verify token validity
   * 3. Load user from database
   * 4. Attach user to request
   * 5. Continue to next handler
   */
  async authenticate(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      // Step 1: Get token from cookie
      const token = req.cookies['access-token'];

      if (!token) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
      }

      // Step 2: Verify token
      const payload = authService.verifyToken(token);

      // Step 3: Load user
      const user = await this.userRepo.findById(payload.userId);
      if (!user) {
        res.status(401).json({ error: 'User not found' });
        return;
      }

      // Step 4: Attach to request
      req.user = {
        id: user.id,
        email: user.email,
        role: user.role
      };

      // Step 5: Continue
      next();
    } catch (error) {
      console.error('Auth error:', error);
      res.status(401).json({ error: 'Invalid token' });
    }
  }

  /**
   * Middleware to require specific role
   */
  requireRole(role: string) {
    return (req: Request, res: Response, next: NextFunction) => {
      if (!req.user) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
      }

      if (req.user.role !== role) {
        res.status(403).json({ error: 'Forbidden' });
        return;
      }

      next();
    };
  }
}

export const authMiddleware = new AuthMiddleware();
