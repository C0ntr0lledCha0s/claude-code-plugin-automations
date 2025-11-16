/**
 * User API Routes
 *
 * RESTful endpoints for user management.
 */

import { Router, Request, Response } from 'express';
import { authMiddleware } from '../auth/authMiddleware';
import { UserRepository } from '../auth/userRepository';

export class UserRoutes {
  router: Router;
  private userRepo: UserRepository;

  constructor() {
    this.router = Router();
    this.userRepo = new UserRepository();
    this.setupRoutes();
  }

  private setupRoutes() {
    // GET /api/users - List users (requires auth)
    this.router.get('/',
      authMiddleware.authenticate.bind(authMiddleware),
      this.listUsers.bind(this)
    );

    // GET /api/users/:id - Get single user (requires auth)
    this.router.get('/:id',
      authMiddleware.authenticate.bind(authMiddleware),
      this.getUser.bind(this)
    );

    // POST /api/users - Create user (admin only)
    this.router.post('/',
      authMiddleware.authenticate.bind(authMiddleware),
      authMiddleware.requireRole('admin'),
      this.createUser.bind(this)
    );

    // PUT /api/users/:id - Update user (admin only)
    this.router.put('/:id',
      authMiddleware.authenticate.bind(authMiddleware),
      authMiddleware.requireRole('admin'),
      this.updateUser.bind(this)
    );

    // DELETE /api/users/:id - Delete user (admin only)
    this.router.delete('/:id',
      authMiddleware.authenticate.bind(authMiddleware),
      authMiddleware.requireRole('admin'),
      this.deleteUser.bind(this)
    );
  }

  /**
   * List all users
   */
  async listUsers(req: Request, res: Response): Promise<void> {
    try {
      const limit = parseInt(req.query.limit as string) || 10;
      const offset = parseInt(req.query.offset as string) || 0;

      const users = await this.userRepo.list(limit, offset);

      // Remove sensitive data
      const sanitized = users.map(u => ({
        id: u.id,
        email: u.email,
        name: u.name,
        role: u.role,
        createdAt: u.createdAt
      }));

      res.json({ users: sanitized, count: sanitized.length });
    } catch (error) {
      console.error('List users error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  /**
   * Get single user
   */
  async getUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await this.userRepo.findById(id);

      if (!user) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      // Remove sensitive data
      const sanitized = {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        createdAt: user.createdAt
      };

      res.json({ user: sanitized });
    } catch (error) {
      console.error('Get user error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  /**
   * Create new user
   */
  async createUser(req: Request, res: Response): Promise<void> {
    try {
      const { email, name, role, password } = req.body;

      // Validation
      if (!email || !name || !password) {
        res.status(400).json({ error: 'Missing required fields' });
        return;
      }

      // Check if user exists
      const existing = await this.userRepo.findByEmail(email);
      if (existing) {
        res.status(409).json({ error: 'User already exists' });
        return;
      }

      // Hash password and create user
      const { authService } = await import('../services/authService');
      const passwordHash = await authService.hashPassword(password);

      const user = await this.userRepo.create({
        email,
        name,
        role: role || 'user',
        passwordHash
      });

      res.status(201).json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        }
      });
    } catch (error) {
      console.error('Create user error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  /**
   * Update user
   */
  async updateUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const updates = req.body;

      // Don't allow password updates here
      delete updates.passwordHash;
      delete updates.id;

      const user = await this.userRepo.update(id, updates);

      if (!user) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      res.json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        }
      });
    } catch (error) {
      console.error('Update user error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  /**
   * Delete user
   */
  async deleteUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const deleted = await this.userRepo.delete(id);

      if (!deleted) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      res.status(204).send();
    } catch (error) {
      console.error('Delete user error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
