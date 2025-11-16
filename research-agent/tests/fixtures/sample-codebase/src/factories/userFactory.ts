/**
 * User Factory Pattern
 *
 * Creational design pattern for creating user objects based on role.
 */

export interface User {
  id: string;
  name: string;
  role: string;
  permissions: string[];
}

export class AdminUser implements User {
  id: string;
  name: string;
  role = 'admin';
  permissions = ['read', 'write', 'delete', 'manage'];

  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }

  manageUsers() {
    console.log('Managing users...');
  }
}

export class RegularUser implements User {
  id: string;
  name: string;
  role = 'user';
  permissions = ['read'];

  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }
}

export class UserFactory {
  /**
   * Factory method to create users based on role
   */
  static createUser(role: string, id: string, name: string): User {
    switch(role) {
      case 'admin':
        return new AdminUser(id, name);
      case 'user':
        return new RegularUser(id, name);
      default:
        throw new Error(`Unknown role: ${role}`);
    }
  }
}
