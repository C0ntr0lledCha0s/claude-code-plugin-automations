# Research Caching Guide

How to use the research cache system to preserve findings and avoid redundant research.

## Overview

The research cache stores research findings across sessions, building institutional knowledge over time and improving efficiency by reusing valid research.

**Benefits**:
- **Avoid Redundant Research**: Don't re-research the same topics
- **Build Knowledge Base**: Accumulate understanding over time
- **Team Sharing**: Share research findings across team members
- **Faster Responses**: Reuse existing research when still valid
- **Historical Tracking**: See how understanding evolved

---

## Cache Structure

```
research-agent/
└── .research-cache/
    ├── investigations/      # Codebase investigations
    ├── best-practices/      # Best practice research
    ├── patterns/            # Pattern analysis
    └── comparisons/         # Technology comparisons
```

Each cached research is a markdown file with YAML frontmatter containing metadata.

---

## Cache Entry Format

Every cache entry includes:

### Metadata (YAML Frontmatter)

```yaml
---
research_type: investigation
topic: user authentication
date: 2025-01-15
expiry: 2025-02-15
codebase_hash: abc123def456
tags: [auth, jwt, security]
related_files:
  - src/auth/middleware.ts
  - src/utils/jwt.ts
---
```

**Fields**:
- `research_type`: Type of research (investigation, best-practice, pattern, comparison)
- `topic`: Research topic or question
- `date`: When research was conducted (YYYY-MM-DD)
- `expiry`: When cache entry expires (default: 30 days)
- `codebase_hash`: Git commit hash (for invalidation if code changes)
- `tags`: Keywords for searching
- `related_files`: Files referenced in research (for change detection)

### Content

Following the frontmatter, the actual research content in markdown format.

---

## Using the Cache

### Command-Line Interface

The cache is managed via `cache-manager.py`:

#### List Cache Entries

```bash
# List all cache entries
python3 scripts/cache-manager.py list

# List by category
python3 scripts/cache-manager.py list investigations

# Hide expired entries
python3 scripts/cache-manager.py list --hide-expired

# Verbose output
python3 scripts/cache-manager.py list -v
```

**Example Output**:
```
Found 12 cache entries:

✓ [investigations] user authentication
   ID: user-authentication-2025-01-15
   Date: 2025-01-15
   Tags: auth, jwt, security

⏰ EXPIRED [best-practices] React hooks
   ID: react-hooks-2024-12-10
   Date: 2024-12-10
   Tags: react, hooks
```

#### Search Cache

```bash
# Search by keyword
python3 scripts/cache-manager.py search "authentication"

# Search is case-insensitive and searches:
# - Topic
# - Tags
# - Content
```

#### Show Cache Entry

```bash
# Show full cache entry
python3 scripts/cache-manager.py show user-authentication-2025-01-15
```

**Example Output**:
```
============================================================
Cache Entry: user authentication
============================================================

ID: user-authentication-2025-01-15
Category: investigations
Date: 2025-01-15
Expired: No
Expiry: 2025-02-15
Tags: auth, jwt, security
Related files: src/auth/middleware.ts, src/utils/jwt.ts

============================================================
Content:
============================================================

[Full research content here...]
```

#### Add Cache Entry

```bash
# Add research to cache
python3 scripts/cache-manager.py add investigations \
  "user authentication" \
  research-output.md \
  --tags "auth,jwt,security" \
  --related-files "src/auth/middleware.ts,src/utils/jwt.ts" \
  --codebase-hash "abc123"
```

#### Invalidate Cache Entry

```bash
# Delete a cache entry
python3 scripts/cache-manager.py invalidate user-authentication-2025-01-15
```

#### Clear Cache

```bash
# Clear expired entries
python3 scripts/cache-manager.py clear --expired

# Clear specific category
python3 scripts/cache-manager.py clear --category investigations

# Clear ALL cache (with confirmation)
python3 scripts/cache-manager.py clear --all
```

#### Cache Statistics

```bash
python3 scripts/cache-manager.py stats
```

**Example Output**:
```
============================================================
Research Cache Statistics
============================================================

Total entries: 23
  Active: 18
  Expired: 5

By Category:
  investigations: 8
  best-practices: 10
  patterns: 3
  comparisons: 2

Top Tags:
  react: 7
  security: 5
  auth: 4
  typescript: 3
  performance: 3

Recent Activity:
  2025-01: 12 entries
  2024-12: 8 entries
  2024-11: 3 entries
```

---

## Cache Workflow

### Before Conducting Research

1. **Check for existing research**:
   ```bash
   python3 scripts/cache-manager.py search "authentication"
   ```

2. **Review existing research** (if found):
   ```bash
   python3 scripts/cache-manager.py show user-authentication-2025-01-15
   ```

3. **Decide**:
   - If cache is still valid → use cached research
   - If cache is expired or outdated → conduct new research

### After Conducting Research

1. **Save research output** to a file (e.g., `research-output.md`)

2. **Add to cache**:
   ```bash
   python3 scripts/cache-manager.py add investigations \
     "user authentication system" \
     research-output.md \
     --tags "auth,jwt,middleware" \
     --related-files "src/auth/login.ts,src/auth/middleware.ts"
   ```

3. **Cache is automatically available** for future lookups

---

## Cache Invalidation

Cache entries are automatically invalidated when:

### Time-Based Expiration
- Default: 30 days after creation
- Configurable via `expiry` field in metadata

### Code Change Detection
- If `codebase_hash` is provided, cache is invalid when code changes
- Check with: `git rev-parse HEAD` and compare to cached hash

### Manual Invalidation
```bash
python3 scripts/cache-manager.py invalidate <cache-id>
```

### Clearing Expired Cache
```bash
# Run periodically to clean up
python3 scripts/cache-manager.py clear --expired
```

---

## Best Practices

### What to Cache

✅ **Good candidates for caching**:
- Codebase architecture investigations
- Best practice research for stable topics
- Pattern analysis of stable codebases
- Technology comparisons (frameworks, libraries)
- API design investigations

❌ **Poor candidates for caching**:
- Rapidly changing code analysis
- Time-sensitive information (unless explicitly dated)
- Project-specific implementation details that change frequently

### Cache Naming

Use descriptive topics:
- ✅ Good: `"user authentication with JWT"`
- ✅ Good: `"React hooks best practices 2025"`
- ❌ Bad: `"research 1"`
- ❌ Bad: `"temp"`

### Tagging Strategy

Include multiple relevant tags:
```yaml
tags:
  - technology (e.g., react, typescript, node)
  - domain (e.g., auth, api, state)
  - pattern (e.g., repository, factory, mvc)
  - concern (e.g., security, performance, testing)
```

Example:
```yaml
tags: [react, hooks, state-management, performance, frontend]
```

### Expiry Guidelines

Set appropriate expiry based on volatility:
- **Fast-changing (7-14 days)**: Framework features, beta APIs
- **Normal (30 days)**: General best practices, stable APIs
- **Stable (90 days)**: Design patterns, architectural principles
- **Very stable (365 days)**: Fundamental concepts

Override default with explicit expiry:
```yaml
expiry: 2025-06-15  # 6 months
```

### Related Files

Always include related files for change detection:
```yaml
related_files:
  - src/auth/login.ts
  - src/auth/middleware.ts
  - src/utils/jwt.ts
```

---

## Team Collaboration

### Shared Cache (Git-Tracked)

By default, cache is committed to git for team sharing.

**Pros**:
- Team members benefit from each other's research
- New team members get instant knowledge base
- Research is versioned and auditable

**Cons**:
- Increases repository size
- Might include project-specific details

### Private Cache (Local Only)

To use private cache:

1. Add to `.gitignore`:
   ```
   research-agent/.research-cache/
   ```

2. Each developer maintains their own cache

**Use when**:
- Research contains sensitive information
- Want personal research notes
- Team prefers separate knowledge bases

---

## Example Cache Entry

Here's a complete example:

```markdown
---
research_type: investigation
topic: JWT authentication implementation
date: 2025-01-15
expiry: 2025-02-15
codebase_hash: a1b2c3d4
tags: [auth, jwt, security, middleware]
related_files:
  - src/auth/jwt.ts
  - src/auth/middleware.ts
  - src/auth/login.ts
---

# Investigation: JWT Authentication Implementation

## Summary

The application uses JWT-based authentication with HttpOnly cookies for token storage. Implementation includes access tokens (15 min) and refresh tokens (7 days).

## Implementation Details

### Token Generation

Implementation in `src/auth/jwt.ts:42-88`:

\`\`\`typescript
function generateAccessToken(user: User): string {
  return jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );
}
\`\`\`

### Middleware Protection

Routes are protected via middleware in `src/auth/middleware.ts:25-67`:

[... rest of investigation content ...]

## Security Analysis

✓ Uses HttpOnly cookies (prevents XSS)
✓ Short access token expiry (15 minutes)
✓ Refresh token rotation on use
⚠️ Consider adding rate limiting
⚠️ Add account lockout after failed attempts

## Recommendations

1. Implement rate limiting on auth endpoints
2. Add account lockout mechanism
3. Consider MFA for admin users
4. Log all authentication events

## References

[1] JWT Best Practices - https://datatracker.ietf.org/doc/html/rfc8725
[2] OWASP Authentication - https://owasp.org/...
```

---

## Maintenance

### Regular Cleanup

Run periodically to keep cache clean:

```bash
# Weekly: clear expired entries
python3 scripts/cache-manager.py clear --expired

# Monthly: review and update old entries
python3 scripts/cache-manager.py list -v
```

### Cache Health Check

```bash
# Check statistics
python3 scripts/cache-manager.py stats

# Look for:
# - High expired count → run cleanup
# - Low total count → not using cache effectively
# - Old entries → might need refresh
```

---

## Advanced Usage

### Automated Caching (Future)

Future enhancement: Automatically cache research after completion.

### Cache Synchronization (Future)

Future enhancement: Sync cache across team members via shared storage.

### Smart Cache Lookup (Future)

Future enhancement: Before research, automatically check cache and offer to use/refresh.

---

## Troubleshooting

### "No cache entries found"

The cache is empty. Add entries manually or wait for automatic caching (if implemented).

### "Cache entry not found"

Check cache ID:
```bash
python3 scripts/cache-manager.py list
```

### Cache shows as expired

Either:
1. Manually refresh the research
2. Delete expired entry and re-research

---

## Configuration

### Change Default Expiry

Edit `scripts/cache-manager.py`:

```python
DEFAULT_EXPIRY_DAYS = 30  # Change to desired days
```

### Custom Cache Location

Set `CACHE_DIR` environment variable or modify script.

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
