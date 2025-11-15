---
description: Look up current best practices for a technology, pattern, or implementation approach with recommendations
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
argument-hint: "[technology/pattern/topic]"
model: claude-sonnet-4-5
---

# Best Practice Command

Quickly look up current best practices (as of 2025) for any technology, design pattern, or implementation approach, with context-specific recommendations.

## Arguments

- **`$ARGUMENTS`**: The technology, pattern, or topic to research best practices for (e.g., "React hooks", "API error handling", "database indexing")

## Workflow

When this command is invoked with `/best-practice <topic>`:

1. **Parse Topic**: Understand what best practices are needed
2. **Check Current Implementation**: See if topic is already used in codebase
3. **Research Standards**: Look up current industry best practices (2025)
4. **Gather Recommendations**: Collect official guidelines and community consensus
5. **Contextualize**: Adapt general practices to project context
6. **Provide Examples**: Include code examples and implementation guidance
7. **Cite Sources**: Reference official docs and authoritative resources

## Research Sources

### Priority Order
1. **Official Documentation** - Framework/language official docs
2. **Standards Bodies** - W3C, OWASP, RFC documents
3. **Trusted Resources** - MDN, verified tech blogs, maintainer guidance
4. **Current Community Consensus** - Recent discussions, established patterns

## Examples

### Example Usage 1: Framework Best Practices
```
/best-practice React hooks 2025
```

Expected behavior:
1. Checks for existing hooks usage in project
2. Researches current React hooks best practices:
   - Official React documentation
   - React team recommendations
   - Common patterns and anti-patterns
3. Provides comprehensive guide:

   **Best Practices for React Hooks (2025)**

   #### Core Rules
   - ✓ Only call hooks at top level (not in loops/conditions)
   - ✓ Only call hooks from React functions
   - ✓ Use ESLint plugin: eslint-plugin-react-hooks
   - ✓ Custom hooks should start with "use"

   #### useState Best Practices
   ```tsx
   // ✓ Good: Descriptive names, appropriate initial values
   const [isLoading, setIsLoading] = useState(false);
   const [user, setUser] = useState<User | null>(null);

   // ✗ Avoid: Storing derived state
   const [fullName, setFullName] = useState(''); // Derive instead!
   const fullName = `${firstName} ${lastName}`; // Better
   ```

   #### useEffect Best Practices
   ```tsx
   // ✓ Good: Cleanup functions, specific dependencies
   useEffect(() => {
     const controller = new AbortController();
     fetchData(controller.signal);
     return () => controller.abort(); // Cleanup
   }, [specificDep]); // Precise dependencies

   // ✗ Avoid: Missing dependencies
   useEffect(() => {
     doSomething(prop); // 'prop' not in deps!
   }, []); // ESLint will catch this
   ```

   #### Custom Hooks Best Practices
   ```tsx
   // ✓ Good: Reusable, focused, well-named
   function useFetch<T>(url: string) {
     const [data, setData] = useState<T | null>(null);
     const [loading, setLoading] = useState(true);
     const [error, setError] = useState<Error | null>(null);

     useEffect(() => {
       // Fetch logic with proper cleanup
     }, [url]);

     return { data, loading, error };
   }
   ```

   **Sources**:
   - [React Hooks Documentation](https://react.dev/reference/react)
   - [Rules of Hooks](https://react.dev/warnings/invalid-hook-call-warning)

### Example Usage 2: Security Best Practices
```
/best-practice API authentication security
```

Expected behavior:
1. Checks current auth implementation in project
2. Researches security best practices:
   - OWASP recommendations
   - Industry standards
   - Common vulnerabilities

3. Provides security-focused guide:

   **API Authentication Security Best Practices (2025)**

   #### Authentication Methods (ranked by security)
   1. **OAuth 2.0 / OIDC** - Delegated authorization
   2. **JWT with HttpOnly Cookies** - Secure token storage
   3. **Session-based with Secure Cookies** - Traditional but secure
   4. **API Keys** - For service-to-service only

   #### Critical Security Measures
   ```typescript
   // ✓ Good: Secure JWT implementation
   const token = jwt.sign(payload, SECRET, {
     expiresIn: '15m',        // Short-lived
     algorithm: 'RS256'       // Asymmetric encryption
   });

   // Set in HttpOnly cookie (not localStorage!)
   res.cookie('token', token, {
     httpOnly: true,          // Prevents XSS
     secure: true,            // HTTPS only
     sameSite: 'strict',      // CSRF protection
     maxAge: 900000           // 15 minutes
   });
   ```

   #### Security Checklist
   - [ ] Use HTTPS everywhere (TLS 1.3+)
   - [ ] Implement rate limiting
   - [ ] Validate all inputs
   - [ ] Use HttpOnly cookies for tokens (not localStorage)
   - [ ] Implement CSRF protection
   - [ ] Set appropriate CORS policies
   - [ ] Use strong password hashing (bcrypt, argon2)
   - [ ] Implement MFA for sensitive operations
   - [ ] Log security events
   - [ ] Rotate secrets regularly

   #### Common Vulnerabilities to Avoid
   - ✗ Storing tokens in localStorage (XSS risk)
   - ✗ Long-lived tokens without refresh mechanism
   - ✗ Predictable token generation
   - ✗ Missing token expiration
   - ✗ No rate limiting (brute force risk)

   **Sources**:
   - [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
   - [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

### Example Usage 3: Code Organization
```
/best-practice Next.js project structure
```

Expected behavior:
1. Checks current project structure
2. Researches Next.js official recommendations
3. Provides structure guide:

   **Next.js Project Structure Best Practices (2025)**

   #### Recommended Structure (App Router)
   ```
   /app                          # App Router directory
     /(routes)                   # Route groups (optional)
       /(marketing)
         /about
         /pricing
       /(dashboard)
         /settings
         /profile
     /api                        # API routes
     /components
       /ui                       # Reusable UI components
       /features                 # Feature-specific components
     /lib                        # Utilities, helpers
       /api                      # API client functions
       /utils                    # Pure utility functions
       /hooks                    # Custom React hooks
     /types                      # TypeScript type definitions
     /styles                     # Global styles
   /public                       # Static assets
   /config                       # Configuration files
   /tests                        # Test files
   ```

   #### File Naming Conventions
   - Routes: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
   - Components: `PascalCase.tsx`
   - Utilities: `camelCase.ts`
   - Types: `PascalCase.ts` or `types.ts`

   #### Component Organization
   ```tsx
   // Feature-based grouping (preferred for scale)
   /components
     /auth
       /LoginForm
         LoginForm.tsx
         LoginForm.test.tsx
         LoginForm.styles.ts
     /dashboard
       /StatsCard
         StatsCard.tsx
   ```

   #### Best Practices
   - ✓ Use Server Components by default
   - ✓ Co-locate related files
   - ✓ Separate client/server code clearly
   - ✓ Use TypeScript for type safety
   - ✓ Keep components small and focused

   **Sources**:
   - [Next.js Project Structure](https://nextjs.org/docs/getting-started/project-structure)
   - [Vercel Best Practices](https://vercel.com/docs)

### Example Usage 4: Database Best Practices
```
/best-practice PostgreSQL indexing
```

Expected behavior:
1. Researches database indexing best practices
2. Provides practical guide:

   **PostgreSQL Indexing Best Practices (2025)**

   #### When to Create Indexes
   - ✓ Columns in WHERE clauses frequently
   - ✓ Columns in JOIN conditions
   - ✓ Columns in ORDER BY clauses
   - ✓ Columns used for grouping (GROUP BY)
   - ✓ Foreign keys

   #### Index Types and Usage
   ```sql
   -- B-tree (default, most common)
   CREATE INDEX idx_users_email ON users(email);

   -- Unique index (enforce uniqueness)
   CREATE UNIQUE INDEX idx_users_username ON users(username);

   -- Partial index (conditional, saves space)
   CREATE INDEX idx_active_users ON users(email) WHERE active = true;

   -- Composite index (multiple columns, order matters!)
   CREATE INDEX idx_users_name ON users(last_name, first_name);

   -- GIN index (for JSON, arrays, full-text search)
   CREATE INDEX idx_users_tags ON users USING GIN(tags);

   -- GiST index (for geometric data, full-text)
   CREATE INDEX idx_locations ON places USING GIST(location);
   ```

   #### Best Practices
   - ✓ Index selectivity: High cardinality columns first
   - ✓ Composite index order: Most selective columns first
   - ✓ Monitor index usage: Remove unused indexes
   - ✓ Keep indexes minimal: Each adds write overhead
   - ✓ Use EXPLAIN ANALYZE to verify index usage

   #### Anti-Patterns
   - ✗ Over-indexing: Too many indexes slow writes
   - ✗ Indexing low-cardinality columns (e.g., boolean)
   - ✗ Wrong order in composite indexes
   - ✗ Not updating statistics (VACUUM ANALYZE)

   **Monitoring**:
   ```sql
   -- Check index usage
   SELECT schemaname, tablename, indexname, idx_scan
   FROM pg_stat_user_indexes
   ORDER BY idx_scan;

   -- Find unused indexes
   SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
   ```

   **Sources**:
   - [PostgreSQL Index Documentation](https://www.postgresql.org/docs/current/indexes.html)
   - [Use The Index, Luke](https://use-the-index-luke.com/)

## Output Format

```markdown
# Best Practices: [Topic]

## Current Implementation (if applicable)
[Analysis of how it's currently done in the project]
- Files: `path/to/file.ts:42`
- Assessment: [Brief evaluation]

## Current Best Practices (2025)

### Core Principles
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

### Recommended Approach
[Detailed explanation of best approach]

```[language]
// Code example showing best practice
```

### Do's and Don'ts

#### ✓ Do
- [Recommended practice 1]
- [Recommended practice 2]

#### ✗ Don't
- [Anti-pattern 1]
- [Anti-pattern 2]

### Common Pitfalls
1. **[Pitfall]**: [Why it's problematic]
   - How to avoid: [Solution]

2. **[Pitfall]**: [Why it's problematic]
   - How to avoid: [Solution]

### Implementation Checklist
- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

## Comparison with Current Implementation

| Aspect | Current | Best Practice |
|--------|---------|---------------|
| ...    | ...     | ...           |

## Migration Path (if changing current code)
1. [Step to migrate]
2. [Step to migrate]
3. [Step to migrate]

## Additional Resources
- [Official documentation link]
- [Authoritative guide link]
- [Tool or library link]

## Quick Reference
[Condensed summary of key points for quick lookup]
```

## Important Notes

- Always research **current** practices (2025, not outdated info)
- Cite authoritative sources (official docs, standards bodies)
- Provide context-specific advice, not generic platitudes
- Include code examples in the relevant language/framework
- Balance ideals with pragmatism
- Note trade-offs explicitly
- Consider project constraints and team skills

## Error Handling

### If no topic provided:
```
Error: No topic specified.

Usage: /best-practice <topic>

Examples:
  /best-practice React hooks
  /best-practice API error handling
  /best-practice git workflow
  /best-practice TypeScript error types
```

### If topic is too broad:
Provide overview and ask for specifics:
```
Best Practices: [Broad Topic]

This is a broad topic. Here's an overview of subtopics:
1. [Subtopic 1]
2. [Subtopic 2]
3. [Subtopic 3]

For more specific guidance, try:
  /best-practice [Broad Topic] [Subtopic]

Or I can provide a general overview of all best practices in this area?
```

## Advanced Usage

### Compare with current implementation:
```
/best-practice error handling in src/api
```
Focuses on error handling specifically in the API layer.

### Technology-specific:
```
/best-practice Next.js 15 data fetching
```
Gets practices for specific version.

### Security-focused:
```
/best-practice secure file upload
```
Emphasizes security aspects.

---

**Pro Tip**: Use /best-practice to learn current standards, then /investigate to see how your project compares, then /research for deeper dive into specific approaches.
