/**
 * User Repository Pattern
 *
 * Abstracts database access for user entities.
 */

export interface UserEntity {
  id: string;
  email: string;
  name: string;
  role: string;
  passwordHash: string;
  createdAt: Date;
  updatedAt: Date;
}

export class UserRepository {
  // In-memory storage for demo (would be database in production)
  private users: Map<string, UserEntity> = new Map();

  /**
   * Find user by email
   */
  async findByEmail(email: string): Promise<UserEntity | null> {
    for (const user of this.users.values()) {
      if (user.email === email) {
        return user;
      }
    }
    return null;
  }

  /**
   * Find user by ID
   */
  async findById(id: string): Promise<UserEntity | null> {
    return this.users.get(id) || null;
  }

  /**
   * Create new user
   */
  async create(user: Omit<UserEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<UserEntity> {
    const id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newUser: UserEntity = {
      ...user,
      id,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.users.set(id, newUser);
    return newUser;
  }

  /**
   * Update user
   */
  async update(id: string, updates: Partial<UserEntity>): Promise<UserEntity | null> {
    const user = this.users.get(id);
    if (!user) {
      return null;
    }

    const updated: UserEntity = {
      ...user,
      ...updates,
      id: user.id, // Prevent ID change
      updatedAt: new Date()
    };

    this.users.set(id, updated);
    return updated;
  }

  /**
   * Delete user
   */
  async delete(id: string): Promise<boolean> {
    return this.users.delete(id);
  }

  /**
   * List all users (with pagination)
   */
  async list(limit: number = 10, offset: number = 0): Promise<UserEntity[]> {
    return Array.from(this.users.values()).slice(offset, offset + limit);
  }
}
