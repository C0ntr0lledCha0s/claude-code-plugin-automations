# Sample Codebase for Research Agent Testing

This is a minimal Node.js/TypeScript codebase used for testing the research-agent plugin's investigation, pattern analysis, and best practices capabilities.

## Purpose

This codebase contains intentional design patterns and architecture that tests can validate the research-agent identifies correctly.

## Design Patterns Included

### 1. Factory Pattern
**Location**: `src/factories/userFactory.ts`
- **Pattern**: Creational - Factory Method
- **Purpose**: Create user objects based on role
- **Classes**: `UserFactory`, `AdminUser`, `RegularUser`

### 2. Singleton Pattern
**Location**: `src/services/authService.ts`
- **Pattern**: Creational - Singleton
- **Purpose**: Ensure single instance of authentication service
- **Class**: `AuthService`
- **Features**: JWT generation, password hashing

### 3. Repository Pattern
**Location**: `src/auth/userRepository.ts`
- **Pattern**: Structural - Repository
- **Purpose**: Abstract database access for users
- **Class**: `UserRepository`
- **Methods**: `findByEmail`, `findById`, `create`, `update`, `delete`, `list`

## Architecture Features

### Authentication Flow
**Components**:
- `src/auth/loginHandler.ts` - Login request handler
- `src/auth/authMiddleware.ts` - JWT authentication middleware
- `src/services/authService.ts` - Token and password management

**Flow**:
1. User submits credentials → `LoginHandler`
2. Handler validates credentials → `UserRepository`
3. Generate JWT token → `AuthService`
4. Set HTTP-only cookie
5. Protected routes use → `AuthMiddleware`
6. Middleware verifies token → `AuthService`
7. Attach user to request → Continue

### RESTful API
**Location**: `src/api/userRoutes.ts`
- **Pattern**: REST API with middleware
- **Endpoints**:
  - `GET /api/users` - List users (authenticated)
  - `GET /api/users/:id` - Get user (authenticated)
  - `POST /api/users` - Create user (admin only)
  - `PUT /api/users/:id` - Update user (admin only)
  - `DELETE /api/users/:id` - Delete user (admin only)

**Features**:
- Middleware chaining for authentication
- Role-based access control
- Error handling
- Input validation

## Test Scenarios

Research-agent tests should be able to:

1. **Identify Patterns**:
   - Factory pattern in `userFactory.ts`
   - Singleton pattern in `authService.ts`
   - Repository pattern in `userRepository.ts`

2. **Trace Execution Flow**:
   - Login flow from handler → repository → service
   - Middleware flow from request → verification → next

3. **Find Related Components**:
   - Authentication components (loginHandler, authMiddleware, authService, userRepository)
   - API layer (userRoutes) depends on auth components

4. **Identify Best Practices**:
   - JWT authentication with HTTP-only cookies
   - Password hashing with bcrypt
   - Role-based access control
   - Input validation
   - Error handling

5. **Security Analysis**:
   - HttpOnly cookies prevent XSS
   - Passwords are hashed, never stored plain
   - Token expiration (15 minutes)
   - Role-based permissions

## File Structure

```
src/
├── api/
│   └── userRoutes.ts         # RESTful user endpoints
├── auth/
│   ├── authMiddleware.ts     # JWT authentication middleware
│   ├── loginHandler.ts       # Login request handler
│   └── userRepository.ts     # User data access (Repository pattern)
├── services/
│   └── authService.ts        # Auth utilities (Singleton pattern)
└── factories/
    └── userFactory.ts        # User creation (Factory pattern)
```

## Dependencies

- **express**: Web framework
- **jsonwebtoken**: JWT token generation
- **bcrypt**: Password hashing
- **typescript**: Type safety

## Notes for Tests

- All patterns are clearly commented
- Execution flows are documented with step-by-step comments
- File references should match: `src/auth/loginHandler.ts:15-88`
- Security best practices are intentionally demonstrated
- Error handling is present but could be improved (for testing recommendations)
