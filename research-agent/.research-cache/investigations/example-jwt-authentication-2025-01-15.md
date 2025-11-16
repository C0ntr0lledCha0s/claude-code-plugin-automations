---
research_type: investigation
topic: JWT authentication implementation
date: 2025-01-15
expiry: 2025-02-15
codebase_hash: abc123def456
tags: [auth, jwt, security, middleware, example]
related_files:
  - src/auth/jwt.ts
  - src/auth/middleware.ts
  - src/auth/login.ts
---

# Investigation: JWT Authentication Implementation

**NOTE**: This is an example cache entry to demonstrate the caching format.

## Summary

The application uses JWT-based authentication with HttpOnly cookies for token storage. Implementation includes access tokens (15 min expiry) and refresh tokens (7 days expiry).

## Implementation Details

### Token Generation

Implementation in `src/auth/jwt.ts:42-88`:

```typescript
function generateAccessToken(user: User): string {
  return jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );
}

function generateRefreshToken(user: User): string {
  return jwt.sign(
    { userId: user.id },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  );
}
```

Source: `src/auth/jwt.ts:42-88`

### Middleware Protection

Routes are protected via middleware in `src/auth/middleware.ts:25-67`:

```typescript
async function authMiddleware(req: Request, res: Response, next: Next) {
  const token = req.cookies['access-token'];

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(payload.userId);
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

Source: `src/auth/middleware.ts:25-67`

### Login Flow

Handler in `src/auth/login.ts:30-75`:

1. Validate credentials against database
2. Generate access token (15 min)
3. Generate refresh token (7 days)
4. Set both as HttpOnly cookies
5. Return user data

## Architecture

```
Client → POST /api/auth/login
         → validateCredentials()
         → generateAccessToken()
         → generateRefreshToken()
         → setHttpOnlyCookies()
         → return { user }
```

## Security Analysis

### Strengths
✓ **HttpOnly cookies** - Prevents XSS access to tokens
✓ **Short access token expiry** - Limits exposure window (15 min)
✓ **Refresh token rotation** - Tokens rotate on each refresh
✓ **Separate secrets** - Access and refresh use different secrets
✓ **HTTPS enforcement** - Cookies require secure connection

### Weaknesses
⚠️ **No rate limiting** - Login endpoint can be brute-forced
⚠️ **No account lockout** - Multiple failed attempts not blocked
⚠️ **Missing MFA** - No multi-factor authentication option
⚠️ **No audit logging** - Authentication events not logged

## Recommendations

### High Priority
1. **Implement rate limiting** on `/api/auth/login`
   - Limit to 5 attempts per minute per IP
   - Use express-rate-limit or similar

2. **Add account lockout** after failed attempts
   - Lock account after 5 failed attempts
   - Require email verification to unlock

3. **Add audit logging** for all auth events
   - Log successful/failed logins
   - Log token refreshes
   - Alert on suspicious patterns

### Medium Priority
4. **Implement MFA** for admin users
   - TOTP (Time-based One-Time Password)
   - SMS backup option
   - Recovery codes

5. **Add token revocation** mechanism
   - Blacklist for compromised tokens
   - Logout invalidates tokens

## Best Practices Compliance

Comparing against OWASP Authentication guidelines [1]:

| Practice | Status | Implementation |
|----------|--------|----------------|
| Secure password storage | ✓ | bcrypt hashing |
| Session expiration | ✓ | 15 min access, 7 day refresh |
| HttpOnly cookies | ✓ | All tokens in HttpOnly cookies |
| HTTPS enforcement | ✓ | secure flag on cookies |
| Rate limiting | ✗ | **Missing** |
| Account lockout | ✗ | **Missing** |
| MFA support | ✗ | **Missing** |
| Audit logging | ✗ | **Missing** |

## Dependencies

- **jsonwebtoken** (v9.0.2) - JWT creation and verification [2]
- **bcrypt** (v5.1.1) - Password hashing [3]
- **cookie-parser** (v1.4.6) - Cookie handling

## Related Components

- Password validation: `src/auth/validators.ts`
- User model: `src/models/User.ts`
- Auth routes: `src/routes/auth.ts`
- Refresh endpoint: `src/auth/refresh.ts`

## Next Steps

- [ ] Add rate limiting middleware
- [ ] Implement account lockout logic
- [ ] Set up audit logging system
- [ ] Research MFA implementation options
- [ ] Add token revocation support

## References

[1] OWASP Authentication Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
[2] jsonwebtoken npm - https://www.npmjs.com/package/jsonwebtoken
[3] bcrypt npm - https://www.npmjs.com/package/bcrypt
[4] JWT Best Practices RFC - https://datatracker.ietf.org/doc/html/rfc8725

## File References

All file paths are relative to project root:

- Token generation: `src/auth/jwt.ts:42-88`
- Authentication middleware: `src/auth/middleware.ts:25-67`
- Login handler: `src/auth/login.ts:30-75`
- Password validation: `src/auth/validators.ts:15-42`

---

**Investigation Date**: 2025-01-15
**Cache Expiry**: 2025-02-15
**Codebase Hash**: abc123def456
